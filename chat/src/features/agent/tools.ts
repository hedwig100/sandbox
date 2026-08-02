import { randomUUID } from "node:crypto";
import { z } from "zod";
import { destinations } from "../trip/catalog";
import type { TripEvent, TripState } from "../trip/types";

const preferenceInput = z.object({ destination: z.string().optional(), dates: z.object({ start: z.string(), end: z.string() }).optional(), travelers: z.number().int().positive().optional(), interests: z.array(z.string()).optional(), budgetLimit: z.number().positive().optional() });
const searchInput = z.object({ interests: z.array(z.string()).default([]), season: z.string().optional(), maxDailyCost: z.number().positive().optional() });
const focusInput = z.object({ destinationId: z.string() });
const itineraryInput = z.object({ day: z.number().int().positive(), time: z.string(), title: z.string().min(1), location: z.string().min(1), note: z.string().default(""), estimatedCost: z.number().nonnegative() });
const budgetInput = z.object({ transport: z.number().nonnegative().optional(), stay: z.number().nonnegative().optional(), food: z.number().nonnegative().optional(), activities: z.number().nonnegative().optional() }).refine((value) => Object.keys(value).length > 0);

export const toolLabels: Record<string, string> = {
  set_trip_preferences: "旅の条件を更新",
  search_destinations: "行き先を検索",
  focus_destination: "候補をピックアップ",
  add_to_itinerary: "旅程に追加",
  update_budget: "予算を更新",
};

export const toolDefinitions = [
  { type: "function", name: "set_trip_preferences", description: "Set or update trip dates, travelers, interests, destination hint, and total budget.", parameters: { type: "object", properties: { destination: { type: "string" }, dates: { type: "object", properties: { start: { type: "string" }, end: { type: "string" } }, required: ["start", "end"], additionalProperties: false }, travelers: { type: "integer", minimum: 1 }, interests: { type: "array", items: { type: "string" } }, budgetLimit: { type: "number", minimum: 1 } }, required: [], additionalProperties: false }, strict: false },
  { type: "function", name: "search_destinations", description: "Search the illustrative catalog for matching Japanese destinations.", parameters: { type: "object", properties: { interests: { type: "array", items: { type: "string" } }, season: { type: "string" }, maxDailyCost: { type: "number", minimum: 1 } }, required: ["interests"], additionalProperties: false }, strict: false },
  { type: "function", name: "focus_destination", description: "Focus one destination already present in candidates.", parameters: { type: "object", properties: { destinationId: { type: "string" } }, required: ["destinationId"], additionalProperties: false }, strict: true },
  { type: "function", name: "add_to_itinerary", description: "Add one concrete item to a numbered trip day.", parameters: { type: "object", properties: { day: { type: "integer", minimum: 1 }, time: { type: "string" }, title: { type: "string" }, location: { type: "string" }, note: { type: "string" }, estimatedCost: { type: "number", minimum: 0 } }, required: ["day", "time", "title", "location", "note", "estimatedCost"], additionalProperties: false }, strict: true },
  { type: "function", name: "update_budget", description: "Update estimated trip budget categories in Japanese yen.", parameters: { type: "object", properties: { transport: { type: "number", minimum: 0 }, stay: { type: "number", minimum: 0 }, food: { type: "number", minimum: 0 }, activities: { type: "number", minimum: 0 } }, required: [], additionalProperties: false }, strict: false },
] as const;

export type ToolResult = { output: string; events: TripEvent[] };
const eventId = () => randomUUID();

export function executeTool(name: string, raw: unknown, state: TripState): ToolResult {
  switch (name) {
    case "set_trip_preferences": { const value = preferenceInput.parse(raw); return { output: `旅行条件を更新しました: ${JSON.stringify(value)}`, events: [{ id: eventId(), type: "preferences.updated", payload: value }] }; }
    case "search_destinations": {
      const value = searchInput.parse(raw);
      const ranked = destinations.map((destination, index) => ({ destination, score: value.interests.filter((interest) => destination.interests.includes(interest)).length * 3 + (value.season && destination.seasons.includes(value.season) ? 2 : 0) - index / 100 })).filter(({ destination }) => !value.maxDailyCost || destination.estimatedDailyCost <= value.maxDailyCost).sort((a, b) => b.score - a.score).slice(0, 3).map(({ destination }) => destination);
      return { output: `${ranked.map((item) => item.city).join("、")}を候補にしました。価格はサンプル概算です。`, events: [{ id: eventId(), type: "candidates.replaced", payload: ranked }] };
    }
    case "focus_destination": { const value = focusInput.parse(raw); if (!state.candidates.some((item) => item.id === value.destinationId)) throw new Error("指定された旅行先は現在の候補にありません"); return { output: `${value.destinationId}を注目候補にしました。`, events: [{ id: eventId(), type: "destination.focused", payload: value }] }; }
    case "add_to_itinerary": { const value = itineraryInput.parse(raw); return { output: `${value.title}を${value.day}日目へ追加しました。`, events: [{ id: eventId(), type: "itinerary.itemAdded", payload: { id: eventId(), ...value } }] }; }
    case "update_budget": { const value = budgetInput.parse(raw); return { output: `予算内訳を更新しました: ${JSON.stringify(value)}`, events: [{ id: eventId(), type: "budget.updated", payload: value }] }; }
    default: throw new Error(`利用できないツールです: ${name}`);
  }
}
