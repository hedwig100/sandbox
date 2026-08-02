# Agentic Travel Chat Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a polished Next.js chat in which a real OpenAI model invokes travel-planning tools that update a typed, responsive travel board.

**Architecture:** A Next.js route owns the OpenAI Responses API loop and executes allow-listed tools against a bundled catalog. Tools return model-facing output plus typed UI events; a client reducer applies those events while the chat renders assistant text and tool activity.

**Tech Stack:** Next.js App Router, React, TypeScript, OpenAI JavaScript SDK, Zod, Vitest, Testing Library, Tailwind CSS.

## Global Constraints

- `OPENAI_API_KEY` is server-only and loaded from `.env.local`.
- Use the current resolved default model `gpt-5.6-sol`, overridable with `OPENAI_MODEL`.
- Use bundled illustrative travel data; do not claim live prices or availability.
- Limit a request to eight tool-call rounds.
- Keep conversation and trip state in browser memory only.
- Do not allow model-generated code or arbitrary state mutations.

---

### Task 1: Application shell and domain contracts

**Files:**
- Create: `package.json`, Next.js/TypeScript/Tailwind/Vitest configuration files
- Create: `src/app/layout.tsx`, `src/app/page.tsx`, `src/app/globals.css`
- Create: `src/features/trip/types.ts`, `src/features/trip/initial-state.ts`
- Test: `src/features/trip/types.test.ts`

**Interfaces:**
- Produces `TripState`, `TripEvent`, `Destination`, `ItineraryItem`, `ToolActivity`, and `initialTripState`.

- [ ] Write a failing contract test that parses the initial state with the exported schema and asserts the default traveler count and empty collections.
- [ ] Run `npm test -- src/features/trip/types.test.ts` and verify the missing module failure.
- [ ] Add the project configuration, schemas, types, initial state, semantic page shell, local fonts/fallbacks, and responsive base styles.
- [ ] Run the focused test and `npm run typecheck`; verify both pass.

### Task 2: Deterministic trip reducer

**Files:**
- Create: `src/features/trip/reducer.ts`
- Test: `src/features/trip/reducer.test.ts`

**Interfaces:**
- Consumes `TripState` and `TripEvent`.
- Produces `applyTripEvent(state: TripState, event: TripEvent): TripState` and `applyTripEvents`.

- [ ] Write failing tests for preference updates, candidate replacement, focus, itinerary insertion, budget updates, and duplicate event IDs.
- [ ] Run the focused test and verify each unsupported event path fails.
- [ ] Implement immutable event application with an `appliedEventIds` collection.
- [ ] Run the reducer suite and typecheck; verify both pass.

### Task 3: Catalog and tool registry

**Files:**
- Create: `src/features/trip/catalog.ts`
- Create: `src/features/agent/tools.ts`
- Test: `src/features/agent/tools.test.ts`

**Interfaces:**
- Consumes `TripState` and validated tool arguments.
- Produces `toolDefinitions` and `executeTool(name, rawArguments, state)` returning `{ output: string; events: TripEvent[] }`.

- [ ] Write failing tests for all five tools, unknown IDs, negative amounts, invalid itinerary days, and deterministic destination ranking.
- [ ] Run the focused suite and verify it fails because the registry is absent.
- [ ] Add a compact Japanese destination catalog and implement Zod-validated `set_trip_preferences`, `search_destinations`, `focus_destination`, `add_to_itinerary`, and `update_budget`.
- [ ] Run the focused suite and typecheck; verify both pass.

### Task 4: Bounded Responses API orchestration

**Files:**
- Create: `src/features/agent/run-agent.ts`
- Create: `src/app/api/chat/route.ts`
- Test: `src/features/agent/run-agent.test.ts`

**Interfaces:**
- Consumes an injected Responses-compatible client, messages, and `TripState`.
- Produces newline-delimited typed stream events: `assistant.delta`, `tool.started`, `tool.completed`, `trip.event`, `response.completed`, and `response.error`.

- [ ] Write failing tests using a minimal injected fake client for direct text, one tool call, sequential tool calls, corrected invalid arguments, provider error mapping, and the eight-round ceiling.
- [ ] Run the focused test and verify orchestration is missing.
- [ ] Implement the Responses API loop using function tools and `function_call_output`, keeping the OpenAI SDK behind a narrow client interface.
- [ ] Implement the POST route, request validation, server-only key checks, NDJSON response, safe errors, and abort propagation.
- [ ] Run the server suite and typecheck; verify both pass.

### Task 5: Chat client and streaming state

**Files:**
- Create: `src/features/chat/use-agent-chat.ts`
- Create: `src/features/chat/chat-panel.tsx`
- Create: `src/features/chat/stream.ts`
- Test: `src/features/chat/stream.test.ts`, `src/features/chat/chat-panel.test.tsx`

**Interfaces:**
- Consumes `/api/chat`, chat history, and current `TripState`.
- Produces rendered messages, tool activities, request state, retry, and ordered trip events.

- [ ] Write failing parser tests for split NDJSON chunks and interaction tests for submission, disabled composer, tool disclosure, streamed text, error, and retry.
- [ ] Run focused tests and verify failures occur at missing behavior.
- [ ] Implement the incremental parser and chat hook, preserving partial output and events after interruption.
- [ ] Implement accessible message bubbles, starter prompts, composer, activity disclosure, configuration/provider error cards, and retry.
- [ ] Run focused tests and typecheck; verify both pass.

### Task 6: Reactive travel board and responsive composition

**Files:**
- Create: `src/features/trip/travel-board.tsx`
- Create: `src/features/trip/preferences-card.tsx`
- Create: `src/features/trip/destination-card.tsx`
- Create: `src/features/trip/itinerary.tsx`
- Create: `src/features/trip/budget-card.tsx`
- Modify: `src/app/page.tsx`, `src/app/globals.css`
- Test: `src/features/trip/travel-board.test.tsx`

**Interfaces:**
- Consumes `TripState` and renders all derived board information.
- Produces desktop split-pane and mobile chat/board tabs with update indicators.

- [ ] Write failing component tests for empty state, candidate focus, itinerary groups, budget totals/limit, sample-data disclosure, and mobile tab semantics.
- [ ] Run the focused suite and verify missing UI failures.
- [ ] Implement the focused components and compose them with the chat hook and trip reducer.
- [ ] Add warm editorial styling, responsive layout, keyboard focus, reduced motion, loading treatments, and non-color status cues.
- [ ] Run focused tests, typecheck, and lint; verify all pass.

### Task 7: End-to-end hardening and documentation

**Files:**
- Create: `.env.example`, `README.md`
- Modify: application files only where verification reveals a tested defect

**Interfaces:**
- Documents `OPENAI_API_KEY`, optional `OPENAI_MODEL`, install, test, and run commands.

- [ ] Run `npm test`, `npm run typecheck`, `npm run lint`, and `npm run build`; record and fix only reproducible failures with a failing regression test first.
- [ ] Start the production server and exercise missing-key behavior plus the main desktop/mobile interaction using browser inspection.
- [ ] If a valid key exists, perform one real request that triggers at least two tools; otherwise clearly report that live-provider verification remains dependent on the user’s local key.
- [ ] Verify no secret is present in client bundles, tracked files, logs, or rendered errors.
- [ ] Finish README setup instructions and re-run the complete verification suite.
