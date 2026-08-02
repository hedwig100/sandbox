import { describe, expect, it } from "vitest";
import { initialTripState } from "./initial-state";
import { applyTripEvent } from "./reducer";
import type { Destination, TripEvent } from "./types";

const kyoto: Destination = { id: "kyoto", city: "京都", region: "関西", tagline: "静けさと美食", description: "古都を歩く旅", interests: ["食", "文化"], seasons: ["秋"], estimatedDailyCost: 22000, accent: "#ad5b45", image: "temple" };

describe("applyTripEvent", () => {
  it("applies all supported event kinds without mutating previous state", () => {
    const events: TripEvent[] = [
      { id: "1", type: "preferences.updated", payload: { interests: ["食"], budgetLimit: 150000 } },
      { id: "2", type: "candidates.replaced", payload: [kyoto] },
      { id: "3", type: "destination.focused", payload: { destinationId: "kyoto" } },
      { id: "4", type: "itinerary.itemAdded", payload: { id: "item", day: 1, time: "12:00", title: "昼食", location: "錦市場", note: "", estimatedCost: 4000 } },
      { id: "5", type: "budget.updated", payload: { food: 24000 } },
    ];
    const result = events.reduce(applyTripEvent, initialTripState);

    expect(result.preferences.interests).toEqual(["食"]);
    expect(result.candidates[0]?.city).toBe("京都");
    expect(result.focusedDestinationId).toBe("kyoto");
    expect(result.itinerary[0]?.location).toBe("錦市場");
    expect(result.budget.food).toBe(24000);
    expect(initialTripState.candidates).toEqual([]);
  });

  it("ignores a duplicate event id", () => {
    const event: TripEvent = { id: "same", type: "budget.updated", payload: { food: 10000 } };
    const once = applyTripEvent(initialTripState, event);
    const twice = applyTripEvent(once, { ...event, payload: { food: 99999 } });
    expect(twice.budget.food).toBe(10000);
  });
});
