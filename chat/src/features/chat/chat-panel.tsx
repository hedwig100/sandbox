"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { ArrowUp, Check, Compass, LoaderCircle, RotateCcw, Sparkles, Wrench } from "lucide-react";
import type { ChatMessage, ToolActivity } from "../trip/types";

const starters = ["11月に2人で、食を楽しむ3泊旅行を15万円以内で考えて", "温泉と自然を楽しむ静かな週末を提案して", "アートとカフェを巡る2日間の旅程を作って"];

export function ChatPanel({ messages, activities, isLoading, error, onSend, onRetry }: { messages: ChatMessage[]; activities: ToolActivity[]; isLoading: boolean; error?: string; onSend: (text: string) => void; onRetry: () => void }) {
  const [value, setValue] = useState(""); const end = useRef<HTMLDivElement>(null);
  useEffect(() => end.current?.scrollIntoView({ behavior: "smooth" }), [messages, activities]);
  const submit = (event: FormEvent) => { event.preventDefault(); const prompt = value.trim(); if (!prompt) return; setValue(""); onSend(prompt); };
  return <section className="chatPanel" aria-label="旅行エージェントとの会話">
    <header className="chatHeader"><div className="agentMark"><Sparkles size={17}/></div><div><strong>旅のコンシェルジュ</strong><span><i/> tools ready</span></div></header>
    <div className="conversation" aria-live="polite">
      {messages.length === 0 ? <div className="welcome"><div className="eyebrow"><Compass size={15}/> AI TRAVEL CONCIERGE</div><h1>まだ知らない旅を、<br/><em>会話から。</em></h1><p>行きたい季節、好きなこと、予算。断片的なアイデアから、あなただけの旅を一緒に描きます。</p><div className="starters">{starters.map((starter) => <button key={starter} onClick={() => onSend(starter)}><span>{starter}</span><ArrowUp size={15}/></button>)}</div></div> : messages.map((message) => <div className={`message ${message.role}`} key={message.id}><span className="messageLabel">{message.role === "user" ? "YOU" : "CONCIERGE"}</span><div>{message.content || (isLoading && message.role === "assistant" ? <span className="typing"><i/><i/><i/></span> : null)}</div></div>)}
      {activities.length > 0 && <div className="activity"><div className="activityTitle"><Wrench size={14}/> 旅のボードを更新中</div>{activities.map((item) => <div className="activityRow" key={item.id}>{item.status === "complete" ? <Check size={14}/> : <LoaderCircle className="spin" size={14}/>}<span>{item.label}</span></div>)}</div>}
      {error && <div className="errorCard"><p>{error}</p><button onClick={onRetry}><RotateCcw size={14}/> 再試行</button></div>}
      <div ref={end}/>
    </div>
    <form className="composer" onSubmit={submit}><textarea value={value} onChange={(event) => setValue(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); event.currentTarget.form?.requestSubmit(); } }} placeholder="旅のイメージを話してみてください…" rows={2} disabled={isLoading}/><button aria-label="送信" disabled={isLoading || !value.trim()}>{isLoading ? <LoaderCircle className="spin"/> : <ArrowUp/>}</button><small>Enterで送信 · Shift + Enterで改行</small></form>
  </section>;
}
