import type { Trip, TripEvent } from "../trip/types";

export type AgentStreamEvent =
  | { type: "assistant.delta"; delta: string }
  | { type: "message.started"; userId: string; assistantId: string; createdAt: string }
  | { type: "tool.started"; id: string; name: string; label: string }
  | { type: "tool.completed"; id: string }
  | { type: "trip.event"; event: TripEvent }
  | { type: "trip.snapshot"; trip: Trip }
  | { type: "response.completed" }
  | { type: "response.error"; message: string; code?: string };

export async function* parseNdjsonStream(stream: ReadableStream<Uint8Array>): AsyncGenerator<AgentStreamEvent> {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    buffer += decoder.decode(value, { stream: !done });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) if (line.trim()) yield JSON.parse(line) as AgentStreamEvent;
    if (done) break;
  }
  if (buffer.trim()) yield JSON.parse(buffer) as AgentStreamEvent;
}
