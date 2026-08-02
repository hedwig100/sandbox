import type { TripState } from "./types";

export const initialTripState: TripState = {
  preferences: { travelers: 2, interests: [] },
  candidates: [],
  itinerary: [],
  budget: { transport: 0, stay: 0, food: 0, activities: 0 },
  appliedEventIds: [],
};
