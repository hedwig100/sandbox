import { tripService } from "@/server/trips/runtime"; import { body,jsonError } from "@/server/trips/http";
type C={params:Promise<{tripId:string;itemId:string}>};
export async function PATCH(request:Request,{params}:C){try{const p=await params,value=await body(request);return Response.json(tripService.updateItineraryItem({...value,tripId:p.tripId,itemId:p.itemId,source:"user"} as Parameters<typeof tripService.updateItineraryItem>[0]))}catch(e){return jsonError(e)}}
export async function DELETE(request:Request,{params}:C){try{const p=await params,value=await body(request);return Response.json(tripService.deleteItineraryItem({tripId:p.tripId,itemId:p.itemId,version:Number(value.version),source:"user"}))}catch(e){return jsonError(e)}}
