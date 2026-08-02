import { describe, expect, it } from "vitest";
import { initialTripState } from "./initial-state";
import { tripStateSchema } from "./types";

describe("trip state contract", () => {
  it("starts with two travelers and no planned content", () => {
    const parsed = tripStateSchema.parse(initialTripState);

    expect(parsed.preferences.travelers).toBe(2);
    expect(parsed.candidates).toEqual([]);
    expect(parsed.itinerary).toEqual([]);
    expect(parsed.appliedEventIds).toEqual([]);
  });
});
