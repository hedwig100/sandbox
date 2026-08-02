import {TripWorkspace}from"@/features/trip/trip-workspace";
export default async function TripPage({params}:{params:Promise<{tripId:string}>}){return <TripWorkspace tripId={(await params).tripId}/>}
