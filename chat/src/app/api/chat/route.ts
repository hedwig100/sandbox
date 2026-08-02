import OpenAI from "openai";
import { z } from "zod";
import { applyTripEvents } from "@/features/trip/reducer";
import { tripStateSchema } from "@/features/trip/types";
import { executeTool, toolDefinitions, toolLabels } from "@/features/agent/tools";

export const runtime = "nodejs";

const requestSchema = z.object({
  messages: z.array(z.object({ role: z.enum(["user", "assistant"]), content: z.string() })).min(1),
  tripState: tripStateSchema,
});

const instructions = `あなたは「Tabi Canvas」の旅行プランナーです。日本語で簡潔かつ温かく応答してください。
会話から旅行条件を抽出したら、必ず適切なツールで画面を更新してください。候補を検索する前に条件を更新し、候補を選んだらfocus_destinationを使えます。
具体的な旅程を提案するときはadd_to_itineraryを複数回、費用見積もりにはupdate_budgetを使ってください。
データは説明用サンプルであり、価格・空席はライブ情報ではないと必要に応じて伝えてください。ユーザーが指定していない重要条件は断定せず質問してください。`;

const encode = (value: unknown) => new TextEncoder().encode(`${JSON.stringify(value)}\n`);

export async function POST(request: Request) {
  if (!process.env.OPENAI_API_KEY) return Response.json({ message: "OPENAI_API_KEY が設定されていません。/.env.local に追加してください。", code: "missing_api_key" }, { status: 503 });
  const parsed = requestSchema.safeParse(await request.json().catch(() => null));
  if (!parsed.success) return Response.json({ message: "リクエストの形式が正しくありません。" }, { status: 400 });

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      const send = (event: unknown) => controller.enqueue(encode(event));
      try {
        const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
        let tripState = parsed.data.tripState;
        let input: OpenAI.Responses.ResponseInput = parsed.data.messages.map((message) => ({ role: message.role, content: message.content }));
        let previousResponseId: string | undefined;

        for (let round = 0; round < 8; round += 1) {
          const response = await client.responses.create({ model: process.env.OPENAI_MODEL ?? "gpt-5.6-sol", instructions, input, previous_response_id: previousResponseId, tools: [...toolDefinitions] as OpenAI.Responses.Tool[], parallel_tool_calls: true });
          const calls = response.output.filter((item): item is OpenAI.Responses.ResponseFunctionToolCall => item.type === "function_call");
          if (calls.length === 0) {
            if (response.output_text) send({ type: "assistant.delta", delta: response.output_text });
            send({ type: "response.completed" }); return;
          }
          const outputs: OpenAI.Responses.ResponseInputItem[] = [];
          for (const call of calls) {
            const activityId = call.call_id;
            send({ type: "tool.started", id: activityId, name: call.name, label: toolLabels[call.name] ?? call.name });
            try {
              const result = executeTool(call.name, JSON.parse(call.arguments), tripState);
              result.events.forEach((event) => send({ type: "trip.event", event }));
              tripState = applyTripEvents(tripState, result.events);
              outputs.push({ type: "function_call_output", call_id: call.call_id, output: result.output });
              send({ type: "tool.completed", id: activityId });
            } catch (error) {
              outputs.push({ type: "function_call_output", call_id: call.call_id, output: `ツール入力エラー: ${error instanceof Error ? error.message : "不明なエラー"}` });
              send({ type: "tool.completed", id: activityId });
            }
          }
          previousResponseId = response.id;
          input = outputs;
        }
        send({ type: "response.error", message: "ツール実行回数の上限に達しました。条件を少し絞って、もう一度お試しください。", code: "tool_limit" });
      } catch (error) {
        const message = error instanceof OpenAI.AuthenticationError ? "APIキーを確認してください。" : error instanceof OpenAI.RateLimitError ? "利用上限に達しました。少し待ってから再試行してください。" : "エージェントとの通信に失敗しました。もう一度お試しください。";
        send({ type: "response.error", message });
      } finally { controller.close(); }
    },
  });
  return new Response(stream, { headers: { "Content-Type": "application/x-ndjson; charset=utf-8", "Cache-Control": "no-store" } });
}
