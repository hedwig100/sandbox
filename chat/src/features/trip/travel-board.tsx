"use client";

import { CalendarDays, CircleDollarSign, Clock3, Heart, MapPin, Sparkles, Users } from "lucide-react";
import type { TripState } from "./types";

const yen = (value: number) => new Intl.NumberFormat("ja-JP", { style: "currency", currency: "JPY", maximumFractionDigits: 0 }).format(value);
const art: Record<string, string> = { temple: "⛩", craft: "◌", sea: "≈", onsen: "♨", mountain: "△" };

export function TravelBoard({ state }: { state: TripState }) {
  const total = Object.values(state.budget).reduce((sum, value) => sum + value, 0);
  const days = [...new Set(state.itinerary.map((item) => item.day))];
  return <section className="board" aria-label="旅行プランボード">
    <header className="boardHeader"><div><span className="boardKicker">YOUR TRIP CANVAS</span><h2>{state.preferences.destination || "次の旅を描く"}</h2></div><span className="draftPill"><i/> LIVE PLAN</span></header>
    <div className="boardScroll">
      <div className="preferenceStrip">
        <div><CalendarDays/><span>日程<strong>{state.preferences.dates ? `${state.preferences.dates.start} – ${state.preferences.dates.end}` : "相談中"}</strong></span></div>
        <div><Users/><span>人数<strong>{state.preferences.travelers}名</strong></span></div>
        <div><Heart/><span>興味<strong>{state.preferences.interests.slice(0, 2).join("・") || "これから発見"}</strong></span></div>
      </div>

      <section className="boardSection"><div className="sectionTitle"><span>01</span><h3>行き先候補</h3><small>CURATED FOR YOU</small></div>
        {state.candidates.length === 0 ? <div className="emptyCanvas"><div className="emptySun"><Sparkles/></div><p>会話を始めると、あなたに似合う<br/>行き先がここに並びます。</p></div> : <div className="destinationGrid">{state.candidates.map((destination) => <article key={destination.id} className={`destination ${state.focusedDestinationId === destination.id ? "focused" : ""}`} style={{ "--accent": destination.accent } as React.CSSProperties}><div className="destinationArt"><span>{art[destination.image]}</span><small>{destination.region}</small></div><div className="destinationBody"><div><h4>{destination.city}</h4>{state.focusedDestinationId === destination.id && <span className="pick">PICK</span>}</div><strong>{destination.tagline}</strong><p>{destination.description}</p><footer><span>1日 約 {yen(destination.estimatedDailyCost)}</span><div>{destination.interests.slice(0, 2).map((interest) => <i key={interest}>#{interest}</i>)}</div></footer></div></article>)}</div>}
      </section>

      <div className="lowerGrid"><section className="boardSection itinerarySection"><div className="sectionTitle"><span>02</span><h3>旅の流れ</h3></div>{days.length === 0 ? <p className="softEmpty">行き先が決まったら、日ごとの小さな物語を組み立てます。</p> : days.map((day) => <div className="day" key={day}><b>DAY {String(day).padStart(2,"0")}</b>{state.itinerary.filter((item) => item.day === day).map((item) => <div className="timeline" key={item.id}><span><Clock3/> {item.time}</span><div><strong>{item.title}</strong><small><MapPin/> {item.location}</small></div><em>{yen(item.estimatedCost)}</em></div>)}</div>)}</section>
        <section className="boardSection budgetSection"><div className="sectionTitle"><span>03</span><h3>予算</h3></div><div className="budgetTotal"><CircleDollarSign/><span>現在の概算<strong>{yen(total)}</strong></span></div>{[["交通",state.budget.transport],["宿泊",state.budget.stay],["食事",state.budget.food],["体験",state.budget.activities]].map(([label, amount]) => <div className="budgetRow" key={label}><span>{label}</span><b>{yen(Number(amount))}</b></div>)}{state.preferences.budgetLimit && <div className={`budgetLimit ${total > state.preferences.budgetLimit ? "over" : ""}`}><span>上限 {yen(state.preferences.budgetLimit)}</span><strong>{total > state.preferences.budgetLimit ? `${yen(total-state.preferences.budgetLimit)} 超過` : `${yen(state.preferences.budgetLimit-total)} 余裕`}</strong></div>}</section></div>
      <p className="disclosure">掲載情報と価格は、このデモ用のサンプル概算です。実際の空席・料金ではありません。</p>
    </div>
  </section>;
}
