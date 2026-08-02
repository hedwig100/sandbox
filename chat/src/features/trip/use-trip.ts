"use client";
import { useCallback,useEffect,useState } from "react";
import type { Trip } from "./types";

export function useTrip(tripId:string){const [trip,setTrip]=useState<Trip>();const [status,setStatus]=useState<"loading"|"saved"|"saving"|"error"|"conflict"|"not-found">("loading");const [error,setError]=useState<string>();
  useEffect(()=>{void(async()=>{localStorage.removeItem("tabi-trip-id");const response=await fetch(`/api/trips/${tripId}`);if(response.status===404){setStatus("not-found");return}if(!response.ok)throw new Error();setTrip(await response.json() as Trip);setStatus("saved")})().catch(()=>{setStatus("error");setError("旅行データを読み込めませんでした。");})},[tripId]);
  const request=useCallback(async(path:string,method:string,payload:Record<string,unknown>)=>{if(!trip)return;setStatus("saving");setError(undefined);const response=await fetch(`/api/trips/${trip.id}${path}`,{method,headers:{"Content-Type":"application/json"},body:JSON.stringify({version:trip.version,...payload})});const result=await response.json() as Trip|{message:string;latest?:Trip};if(response.status===409){const e=result as {message:string;latest?:Trip};if(e.latest)setTrip(e.latest);setStatus("conflict");setError("別の更新がありました。最新状態を表示しています。もう一度操作してください。");return}if(!response.ok){setStatus("error");setError((result as {message:string}).message);return}setTrip(result as Trip);setStatus("saved");},[trip]);
  return {trip,status,error,request,replaceTrip:setTrip};}
