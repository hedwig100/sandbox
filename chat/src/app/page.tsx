"use client";

import { useCallback, useReducer, useState } from "react";
import { MessageCircle, PanelsTopLeft } from "lucide-react";
import { ChatPanel } from "@/features/chat/chat-panel";
import { useAgentChat } from "@/features/chat/use-agent-chat";
import { initialTripState } from "@/features/trip/initial-state";
import { applyTripEvent } from "@/features/trip/reducer";
import { TravelBoard } from "@/features/trip/travel-board";
import type { TripEvent } from "@/features/trip/types";

export default function Home() {
  const [tripState, dispatch] = useReducer(applyTripEvent, initialTripState);
  const [tab, setTab] = useState<"chat" | "board">("chat");
  const [boardUpdated, setBoardUpdated] = useState(false);
  const onTripEvent = useCallback((event: TripEvent) => { dispatch(event); if (tab === "chat") setBoardUpdated(true); }, [tab]);
  const chat = useAgentChat(tripState, onTripEvent);
  return <main className={`appShell tab-${tab}`}>
    <nav className="brandRail"><div className="brand">旅<br/><span>CANVAS</span></div><div className="railLine"/><small>AI JOURNEY STUDIO · 2026</small></nav>
    <div className="mobileTabs" role="tablist"><button role="tab" aria-selected={tab === "chat"} onClick={() => setTab("chat")}><MessageCircle/> 会話</button><button role="tab" aria-selected={tab === "board"} onClick={() => { setTab("board"); setBoardUpdated(false); }}><PanelsTopLeft/> ボード {boardUpdated && <i/>}</button></div>
    <ChatPanel {...chat} onSend={chat.send} onRetry={chat.retry}/><TravelBoard state={tripState}/>
  </main>;
}
