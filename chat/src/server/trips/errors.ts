import type { Trip } from "@/features/trip/types";
export class TripError extends Error { constructor(public code: "NOT_FOUND"|"VERSION_CONFLICT"|"INVALID", message: string, public latest?: Trip) { super(message); } }
