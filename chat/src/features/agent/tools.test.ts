import { describe, expect, it } from "vitest";
import { initialTripState } from "../trip/initial-state";
import { executeTool, toolDefinitions } from "./tools";

describe("agent tools", () => {
  it("only marks schemas strict when every property is required", () => {
    for (const tool of toolDefinitions) {
      if (!tool.strict) continue;
      expect(new Set(tool.parameters.required)).toEqual(new Set(Object.keys(tool.parameters.properties)));
    }
  });

  it("updates preferences and returns a typed event", () => {
    const result = executeTool("set_trip_preferences", { travelers: 2, interests: ["食"], budgetLimit: 150000 }, initialTripState);
    expect(result.events[0]).toMatchObject({ type: "preferences.updated", payload: { interests: ["食"] } });
  });

  it("ranks matching destinations deterministically", () => {
    const result = executeTool("search_destinations", { interests: ["食", "文化"], season: "秋", maxDailyCost: 30000 }, initialTripState);
    expect(result.events[0]?.type).toBe("candidates.replaced");
    if (result.events[0]?.type === "candidates.replaced") expect(result.events[0].payload[0]?.id).toBe("kyoto");
  });

  it("rejects unknown focused destinations", () => {
    expect(() => executeTool("focus_destination", { destinationId: "missing" }, initialTripState)).toThrow("候補");
  });

  it("adds an itinerary item and rejects negative cost", () => {
    const valid = executeTool("add_to_itinerary", { day: 1, time: "12:00", title: "ランチ", location: "市場", estimatedCost: 3000 }, initialTripState);
    expect(valid.events[0]?.type).toBe("itinerary.itemAdded");
    expect(() => executeTool("add_to_itinerary", { day: 1, time: "12:00", title: "ランチ", location: "市場", estimatedCost: -1 }, initialTripState)).toThrow();
  });

  it("updates non-negative budget categories", () => {
    const result = executeTool("update_budget", { transport: 40000, stay: 50000, food: 30000, activities: 10000 }, initialTripState);
    expect(result.events[0]).toMatchObject({ type: "budget.updated", payload: { food: 30000 } });
    expect(() => executeTool("update_budget", { food: -1 }, initialTripState)).toThrow();
  });
});
