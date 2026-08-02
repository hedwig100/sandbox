import { tripService } from "@/server/trips/runtime"; import { jsonError } from "@/server/trips/http";
export async function GET(_:Request,{params}:{params:Promise<{tripId:string}>}){try{return Response.json(tripService.getTrip((await params).tripId))}catch(e){return jsonError(e)}}
export async function DELETE(_:Request,{params}:{params:Promise<{tripId:string}>}){try{tripService.deleteTrip((await params).tripId);return new Response(null,{status:204})}catch(e){return jsonError(e)}}
