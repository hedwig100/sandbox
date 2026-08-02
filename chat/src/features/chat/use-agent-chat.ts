"use client";

import { useCallback, useState } from "react";
import { parseNdjsonStream } from "./stream";
import type { ChatMessage, ToolActivity, TripEvent, TripState } from "../trip/types";

export function useAgentChat(tripState: TripState, onTripEvent: (event: TripEvent) => void) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [activities, setActivities] = useState<ToolActivity[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>();
  const [lastPrompt, setLastPrompt] = useState("");

  const send = useCallback(async (text: string) => {
    const clean = text.trim(); if (!clean || isLoading) return;
    setLastPrompt(clean); setError(undefined); setActivities([]); setIsLoading(true);
    const user: ChatMessage = { id: crypto.randomUUID(), role: "user", content: clean };
    const assistantId = crypto.randomUUID();
    const nextMessages = [...messages, user];
    setMessages([...nextMessages, { id: assistantId, role: "assistant", content: "" }]);
    try {
      const response = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: nextMessages.map(({ role, content }) => ({ role, content })), tripState }) });
      if (!response.ok) { const body = await response.json().catch(() => ({})) as { message?: string }; throw new Error(body.message ?? "リクエストに失敗しました。"); }
      if (!response.body) throw new Error("応答ストリームを開始できませんでした。");
      for await (const event of parseNdjsonStream(response.body)) {
        if (event.type === "assistant.delta") setMessages((current) => current.map((message) => message.id === assistantId ? { ...message, content: message.content + event.delta } : message));
        if (event.type === "tool.started") setActivities((current) => [...current, { id: event.id, name: event.name, label: event.label, status: "running" }]);
        if (event.type === "tool.completed") setActivities((current) => current.map((activity) => activity.id === event.id ? { ...activity, status: "complete" } : activity));
        if (event.type === "trip.event") onTripEvent(event.event);
        if (event.type === "response.error") throw new Error(event.message);
      }
    } catch (cause) { setError(cause instanceof Error ? cause.message : "予期しないエラーが発生しました。"); }
    finally { setIsLoading(false); }
  }, [isLoading, messages, onTripEvent, tripState]);

  return { messages, activities, isLoading, error, send, retry: () => send(lastPrompt) };
}
