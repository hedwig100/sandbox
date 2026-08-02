"use client";

import { useCallback, useEffect, useState } from "react";
import { parseNdjsonStream } from "./stream";
import type { ChatMessage, ToolActivity, Trip } from "../trip/types";

export function useAgentChat(trip: Trip | undefined, onTripSnapshot: (trip: Trip) => void) {
  const tripId = trip?.id;
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [activities, setActivities] = useState<ToolActivity[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>();
  const [lastPrompt, setLastPrompt] = useState("");
  useEffect(()=>{if(!tripId)return;void fetch(`/api/trips/${tripId}/chat`).then(async response=>{if(!response.ok)throw new Error();setMessages(await response.json() as ChatMessage[])}).catch(()=>setError("チャット履歴を読み込めませんでした。"))},[tripId]);

  const send = useCallback(async (text: string, retryMessageId?:string) => {
    const clean = text.trim(); if (!clean || isLoading) return;
    setLastPrompt(clean); setError(undefined); setActivities([]); setIsLoading(true);
    const user: ChatMessage = { id: crypto.randomUUID(), role: "user", content: clean };
    const assistantId = crypto.randomUUID();
    const nextMessages = retryMessageId?messages:[...messages, user];
    setMessages([...nextMessages, { id: assistantId, role: "assistant", content: "", status:"pending" }]);
    try {
      if (!trip) throw new Error("旅行データを準備中です。");
      const response = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(retryMessageId?{tripId:trip.id,retryMessageId}:{tripId:trip.id,content:clean}) });
      if (!response.ok) { const body = await response.json().catch(() => ({})) as { message?: string }; throw new Error(body.message ?? "リクエストに失敗しました。"); }
      if (!response.body) throw new Error("応答ストリームを開始できませんでした。");
      for await (const event of parseNdjsonStream(response.body)) {
        if(event.type==="message.started")setMessages(current=>current.map(message=>message.id===assistantId?{...message,id:event.assistantId,createdAt:event.createdAt}:message.id===user.id?{...message,id:event.userId}:message));
        if (event.type === "assistant.delta") setMessages((current) => current.map((message) => message.id === assistantId ? { ...message, content: message.content + event.delta } : message));
        if (event.type === "tool.started") setActivities((current) => [...current, { id: event.id, name: event.name, label: event.label, status: "running" }]);
        if (event.type === "tool.completed") setActivities((current) => current.map((activity) => activity.id === event.id ? { ...activity, status: "complete" } : activity));
        if (event.type === "trip.snapshot") onTripSnapshot(event.trip);
        if (event.type === "response.error") throw new Error(event.message);
      }
    } catch (cause) { setMessages(current=>current.map(message=>message.id===assistantId?{...message,status:"failed"}:message));setError(cause instanceof Error ? cause.message : "予期しないエラーが発生しました。"); }
    finally { setIsLoading(false); }
  }, [isLoading, messages, onTripSnapshot, trip]);

  return { messages, activities, isLoading, error, send, retry: () => send(lastPrompt), retryMessage:(id:string)=>send("再試行",id) };
}
