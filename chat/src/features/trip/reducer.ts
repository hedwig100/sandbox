import type { TripEvent, TripState } from "./types";

export function applyTripEvent(state: TripState, event: TripEvent): TripState {
  if (state.appliedEventIds.includes(event.id)) return state;
  const next = { ...state, appliedEventIds: [...state.appliedEventIds, event.id] };
  switch (event.type) {
    case "preferences.updated":
      return { ...next, preferences: { ...state.preferences, ...event.payload } };
    case "candidates.replaced":
      return { ...next, candidates: event.payload, focusedDestinationId: undefined };
    case "destination.focused":
      return { ...next, focusedDestinationId: event.payload.destinationId };
    case "itinerary.itemAdded":
      return { ...next, itinerary: [...state.itinerary, event.payload].sort((a, b) => a.day - b.day || a.time.localeCompare(b.time)) };
    case "budget.updated":
      return { ...next, budget: { ...state.budget, ...event.payload } };
  }
}

export function applyTripEvents(state: TripState, events: TripEvent[]) {
  return events.reduce(applyTripEvent, state);
}
