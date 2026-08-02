import { describe, expect, it } from "vitest";
import { parseNdjsonStream } from "./stream";

describe("parseNdjsonStream", () => {
  it("parses records split across transport chunks", async () => {
    const encoder = new TextEncoder();
    const stream = new ReadableStream<Uint8Array>({ start(controller) { controller.enqueue(encoder.encode('{"type":"assistant.delta","delta":"こん')); controller.enqueue(encoder.encode('にちは"}\n{"type":"response.completed"}\n')); controller.close(); } });
    const found: unknown[] = [];
    for await (const event of parseNdjsonStream(stream)) found.push(event);
    expect(found).toEqual([{ type: "assistant.delta", delta: "こんにちは" }, { type: "response.completed" }]);
  });
});
