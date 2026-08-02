import { tripService } from "@/server/trips/runtime";
import { jsonError } from "@/server/trips/http";
export async function POST(){try{return Response.json(tripService.createTrip(),{status:201})}catch(e){return jsonError(e)}}
export async function GET(){try{return Response.json(tripService.listTrips())}catch(e){return jsonError(e)}}
