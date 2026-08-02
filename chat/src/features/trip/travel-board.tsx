"use client";
import { FormEvent,useState } from "react";
import { CalendarDays,Check,ChevronDown,ChevronUp,CircleDollarSign,Clock3,MapPin,Plus,Search,Trash2,Users } from "lucide-react";
import type { Trip } from "./types";
const yen=(n:number)=>new Intl.NumberFormat("ja-JP").format(n)+"円";
type Requester=(path:string,method:string,payload:Record<string,unknown>)=>Promise<void>;

export function TravelBoard({state,status,error,onRequest}:{state:Trip;status:string;error?:string;onRequest:Requester}){
 const [newItem,setNewItem]=useState({day:1,time:"10:00",title:"",location:"",note:"",estimatedCost:0});
 const total=Object.values(state.budget).reduce((a,b)=>a+b,0);const days=[...new Set(state.itinerary.map(x=>x.day))];
 const preference=(key:string,value:unknown)=>onRequest("/preferences","PATCH",{[key]:value});
 const add=async(e:FormEvent)=>{e.preventDefault();if(!newItem.title||!newItem.location)return;await onRequest("/itinerary","POST",newItem);setNewItem({...newItem,title:"",location:"",note:"",estimatedCost:0})};
 const move=async(id:string,direction:-1|1)=>{const items=[...state.itinerary];const index=items.findIndex(x=>x.id===id),target=index+direction;if(target<0||target>=items.length)return;[items[index],items[target]]=[items[target],items[index]];await onRequest("/itinerary/reorder","POST",{items:items.map((x,position)=>({id:x.id,day:x.day,position}))})};
 return <section className="board" aria-label="編集可能な旅行プラン">
  <header className="boardHeader"><div><span className="boardKicker">COLLABORATIVE TRIP</span><h2>{state.preferences.destination||"次の旅を描く"}</h2></div><span className={`draftPill status-${status}`}>{status==="saving"?"保存中…":status==="conflict"?"競合あり":"保存済み"}</span></header>
  <div className="boardScroll">{error&&<div className="workspaceError">{error}</div>}
   <section className="editorCard"><div className="sectionTitle"><span>01</span><h3>旅行条件</h3><small>USER + AGENT</small></div><div className="editorGrid">
    <label>行き先<input defaultValue={state.preferences.destination} onBlur={e=>void preference("destination",e.target.value)}/></label>
    <label><Users/>人数<input type="number" min="1" defaultValue={state.preferences.travelers} onBlur={e=>void preference("travelers",Number(e.target.value))}/></label>
    <label><CalendarDays/>開始日<input type="date" defaultValue={state.preferences.dates?.start} onBlur={e=>void preference("dates",{start:e.target.value,end:state.preferences.dates?.end||e.target.value})}/></label>
    <label>終了日<input type="date" defaultValue={state.preferences.dates?.end} onBlur={e=>void preference("dates",{start:state.preferences.dates?.start||e.target.value,end:e.target.value})}/></label>
    <label>興味<input defaultValue={state.preferences.interests.join("、")} onBlur={e=>void preference("interests",e.target.value.split(/[、,]/).map(x=>x.trim()).filter(Boolean))}/></label>
    <label>総予算<input type="number" min="1" defaultValue={state.preferences.budgetLimit} onBlur={e=>void preference("budgetLimit",Number(e.target.value))}/></label>
   </div></section>
   <section className="editorCard"><div className="sectionTitle"><span>02</span><h3>行き先候補</h3><button className="miniButton" onClick={()=>void onRequest("/candidates/search","POST",{interests:state.preferences.interests})}><Search/>候補を検索</button></div><div className="destinationGrid">{state.candidates.map(c=><button key={c.id} className={`destination candidateButton ${state.focusedDestinationId===c.id?"focused":""}`} onClick={()=>void onRequest(`/candidates/${c.id}`,"PATCH",{})}><div className="destinationArt" style={{background:c.accent}}><strong>{c.city}</strong><small>{c.region}</small></div><div className="destinationBody"><b>{c.tagline}</b><span className={`sourceBadge ${c.source}`}>{c.source==="agent"?"AI":"YOU"}</span></div></button>)}</div></section>
   <section className="editorCard"><div className="sectionTitle"><span>03</span><h3>旅の流れ</h3></div>{days.map(day=><div className="day" key={day}><b>DAY {day}</b>{state.itinerary.filter(x=>x.day===day).map(item=><div className="timeline editableTimeline" key={item.id}><span><Clock3/>{item.time}</span><div><input aria-label="予定名" defaultValue={item.title} onBlur={e=>void onRequest(`/itinerary/${item.id}`,"PATCH",{title:e.target.value})}/><small><MapPin/>{item.location}</small></div><span className={`sourceBadge ${item.source}`}>{item.source==="agent"?"AI":"YOU"}</span><div className="itemActions"><button aria-label="上へ" onClick={()=>void move(item.id,-1)}><ChevronUp/></button><button aria-label="下へ" onClick={()=>void move(item.id,1)}><ChevronDown/></button><button aria-label="削除" onClick={()=>void onRequest(`/itinerary/${item.id}`,"DELETE",{})}><Trash2/></button></div></div>)}</div>)}
    <form className="addItem" onSubmit={add}><input type="number" min="1" aria-label="日" value={newItem.day} onChange={e=>setNewItem({...newItem,day:Number(e.target.value)})}/><input type="time" aria-label="時刻" value={newItem.time} onChange={e=>setNewItem({...newItem,time:e.target.value})}/><input placeholder="予定" value={newItem.title} onChange={e=>setNewItem({...newItem,title:e.target.value})}/><input placeholder="場所" value={newItem.location} onChange={e=>setNewItem({...newItem,location:e.target.value})}/><input type="number" min="0" placeholder="費用" value={newItem.estimatedCost} onChange={e=>setNewItem({...newItem,estimatedCost:Number(e.target.value)})}/><button><Plus/>追加</button></form>
   </section>
   <section className="editorCard"><div className="sectionTitle"><span>04</span><h3>予算</h3></div><div className="budgetTotal"><CircleDollarSign/><span>現在の概算<strong>{yen(total)}</strong></span></div><div className="budgetEditGrid">{(["transport","stay","food","activities"] as const).map(key=><label key={key}>{({transport:"交通",stay:"宿泊",food:"食事",activities:"体験"})[key]}<input type="number" min="0" defaultValue={state.budget[key]} onBlur={e=>void onRequest("/budget","PATCH",{[key]:Number(e.target.value)})}/></label>)}</div>{state.preferences.budgetLimit&&<p className={total>state.preferences.budgetLimit?"overText":"underText"}><Check/>{total>state.preferences.budgetLimit?`${yen(total-state.preferences.budgetLimit)} 超過`:`${yen(state.preferences.budgetLimit-total)} 余裕`}</p>}</section>
  </div>
 </section>;
}
