import { z } from "zod";

export const destinationSchema = z.object({
  id: z.string(),
  city: z.string(),
  region: z.string(),
  tagline: z.string(),
  description: z.string(),
  interests: z.array(z.string()),
  seasons: z.array(z.string()),
  estimatedDailyCost: z.number().nonnegative(),
  accent: z.string(),
  image: z.string(),
});

export const itineraryItemSchema = z.object({
  id: z.string(),
  day: z.number().int().positive(),
  time: z.string(),
  title: z.string(),
  location: z.string(),
  note: z.string().default(""),
  estimatedCost: z.number().nonnegative(),
});

export const tripPreferencesSchema = z.object({
  destination: z.string().optional(),
  dates: z.object({ start: z.string(), end: z.string() }).optional(),
  travelers: z.number().int().positive(),
  interests: z.array(z.string()),
  budgetLimit: z.number().positive().optional(),
});

export const budgetSchema = z.object({
  transport: z.number().nonnegative(),
  stay: z.number().nonnegative(),
  food: z.number().nonnegative(),
  activities: z.number().nonnegative(),
});

export const tripStateSchema = z.object({
  preferences: tripPreferencesSchema,
  candidates: z.array(destinationSchema),
  focusedDestinationId: z.string().optional(),
  itinerary: z.array(itineraryItemSchema),
  budget: budgetSchema,
  appliedEventIds: z.array(z.string()),
});

export type Destination = z.infer<typeof destinationSchema>;
export type ItineraryItem = z.infer<typeof itineraryItemSchema>;
export type TripPreferences = z.infer<typeof tripPreferencesSchema>;
export type Budget = z.infer<typeof budgetSchema>;
export type TripState = z.infer<typeof tripStateSchema>;

type EventBase = { id: string };
export type TripEvent =
  | (EventBase & { type: "preferences.updated"; payload: Partial<TripPreferences> })
  | (EventBase & { type: "candidates.replaced"; payload: Destination[] })
  | (EventBase & { type: "destination.focused"; payload: { destinationId: string } })
  | (EventBase & { type: "itinerary.itemAdded"; payload: ItineraryItem })
  | (EventBase & { type: "budget.updated"; payload: Partial<Budget> });

export type ChatMessage = { id: string; role: "user" | "assistant"; content: string };
export type ToolActivity = { id: string; name: string; status: "running" | "complete" | "error"; label: string };
