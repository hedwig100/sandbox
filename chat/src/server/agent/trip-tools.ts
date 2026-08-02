import type { Trip } from "@/features/trip/types";
import { executeTool as validateLegacyTool, toolDefinitions, toolLabels } from "@/features/agent/tools";
import type { TripService } from "@/server/trips/service";

export { toolDefinitions, toolLabels };
export function executeTripTool(name:string,raw:unknown,context:{tripId:string;trip:Trip;service:TripService}){
  const legacy=validateLegacyTool(name,raw,{...context.trip,appliedEventIds:[]}); const event=legacy.events[0]; if(!event)return {output:legacy.output,trip:context.trip};
  const base={tripId:context.tripId,version:context.trip.version,source:"agent" as const}; let trip:Trip;
  switch(event.type){case "preferences.updated":trip=context.service.updatePreferences({...base,...event.payload});break;case "candidates.replaced":{const value=raw as {interests?:string[];season?:string;maxDailyCost?:number};trip=context.service.searchCandidates({...base,interests:value.interests??[],season:value.season,maxDailyCost:value.maxDailyCost});break}case "destination.focused":trip=context.service.selectCandidate({...base,destinationId:event.payload.destinationId});break;case "itinerary.itemAdded":{const item=event.payload;trip=context.service.createItineraryItem({...base,day:item.day,time:item.time,title:item.title,location:item.location,note:item.note,estimatedCost:item.estimatedCost});break}case "budget.updated":trip=context.service.updateBudget({...base,...event.payload});break;}
  return {output:`${legacy.output} 現在のversionは${trip.version}です。`,trip};
}
