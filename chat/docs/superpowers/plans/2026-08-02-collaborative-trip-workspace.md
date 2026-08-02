# Collaborative Trip Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist trips in SQLite and let users and the OpenAI agent perform equivalent, version-safe edits through one TripService.

**Architecture:** Drizzle owns normalized SQLite storage, while TripService owns mutations, transactions, ordering, provenance, and optimistic-concurrency checks. REST handlers and agent tools share TripService; the client reconciles complete canonical Trip responses and provides editable controls.

**Tech Stack:** Next.js App Router, TypeScript, Drizzle ORM, better-sqlite3, Zod, OpenAI Responses API, React, Vitest, Testing Library.

## Global Constraints

- SQLite is the canonical trip state and the runtime database file is ignored by Git.
- Browser mutations force `source: "user"`; agent tools force `source: "agent"`.
- Every mutation requires the expected trip `version` and increments it exactly once.
- Version conflicts return HTTP 409 with the latest canonical trip.
- REST handlers and agent tools do not issue SQL or loopback HTTP requests.
- Existing sample catalog data remains illustrative and non-live.
- No authentication, shared users, WebSockets, external travel APIs, booking, or payments.

---

### Task 1: Database schema and canonical Trip contracts

**Files:**
- Modify: `package.json`, `.gitignore`, `src/features/trip/types.ts`, `src/features/trip/initial-state.ts`
- Create: `drizzle.config.ts`, `src/server/db/schema.ts`, `src/server/db/client.ts`, `src/server/db/migrate.ts`, `drizzle/0000_collaborative_trips.sql`
- Test: `src/server/trips/repository.test.ts`

**Interfaces:**
- Produces `Trip`, `TripCandidate`, source-aware `ItineraryItem`, Drizzle tables, `createDatabase(path)` and migration setup.

- [ ] Write a failing temporary-SQLite test that migrates, creates a trip row plus budget, and reads its normalized children.
- [ ] Run the focused test and verify missing database modules cause failure.
- [ ] Install Drizzle and SQLite dependencies, define schemas/contracts, migrations, DB factory, and Git ignores.
- [ ] Run the focused test and typecheck until both pass.

### Task 2: Versioned TripService

**Files:**
- Create: `src/server/trips/errors.ts`, `src/server/trips/repository.ts`, `src/server/trips/service.ts`, `src/server/trips/service.test.ts`

**Interfaces:**
- Produces `createTrip`, `getTrip`, `updatePreferences`, `searchCandidates`, `selectCandidate`, `createItineraryItem`, `updateItineraryItem`, `deleteItineraryItem`, `reorderItinerary`, and `updateBudget`.
- Every mutation consumes `{ tripId, version, source, ...fields }` and returns a canonical `Trip`.

- [ ] Write failing tests for creation, persistence, all CRUD operations, provenance, monotonic versions, stale-version conflicts, contiguous ordering, missing resources, and transaction rollback.
- [ ] Run the service tests and verify each missing operation fails for its intended reason.
- [ ] Implement repository hydration and TripService transactions with compare-and-swap version checks.
- [ ] Run service, repository, reducer compatibility, and type tests until green.

### Task 3: REST API

**Files:**
- Create: `src/server/trips/http.ts`
- Create: `src/app/api/trips/route.ts`
- Create: `src/app/api/trips/[tripId]/route.ts`
- Create: preference, candidate, itinerary, reorder, and budget route files under `src/app/api/trips/[tripId]/`
- Test: `src/server/trips/http.test.ts`

**Interfaces:**
- Consumes TripService operations and Zod request schemas.
- Produces JSON canonical trips and stable 400/404/409/500 error payloads.

- [ ] Write failing route-boundary tests for create/read, validation, not found, conflict with latest trip, provenance enforcement, and successful mutation.
- [ ] Run focused tests and verify handler modules are missing.
- [ ] Implement a shared HTTP error mapper and thin App Router handlers.
- [ ] Run focused tests, typecheck, and lint until green.

### Task 4: Agent tool migration

**Files:**
- Modify: `src/features/agent/tools.ts`, `src/features/agent/tools.test.ts`, `src/app/api/chat/route.ts`
- Create: `src/server/agent/trip-tools.ts`, `src/server/agent/trip-tools.test.ts`

**Interfaces:**
- Chat accepts `{ tripId, messages }`.
- Agent tools consume the current trip/version via a per-request tool context and return canonical Trip snapshots to the stream.

- [ ] Write failing equivalence tests proving REST-like service calls and agent tools create identical canonical state, plus a stale-version reread test.
- [ ] Run focused tests and verify the new tool context is absent.
- [ ] Replace client-event tools with TripService-backed tools and emit `trip.snapshot` after each mutation.
- [ ] Update chat route to fetch canonical state, retain newest version across calls, and safely map provider/domain errors.
- [ ] Run agent tests, typecheck, and a real OpenAI tool turn.

### Task 5: Client trip resource and optimistic operations

**Files:**
- Create: `src/features/trip/api.ts`, `src/features/trip/use-trip.ts`, `src/features/trip/use-trip.test.tsx`
- Modify: `src/features/chat/stream.ts`, `src/features/chat/use-agent-chat.ts`, `src/app/page.tsx`

**Interfaces:**
- Produces `useTrip()` with confirmed state, optimistic state, save status, conflict state, `mutate`, `reapply`, and `discard`.
- Chat consumes `tripId`; `trip.snapshot` replaces confirmed state.

- [ ] Write failing tests for initial create/restore, optimistic success, rollback, stale conflict preservation, reapply, discard, and chat snapshot reconciliation.
- [ ] Run focused tests and verify the hook is missing.
- [ ] Implement API calls, browser trip-ID storage, optimistic operation queue, and snapshot reconciliation.
- [ ] Update page/chat integration and run focused tests plus typecheck.

### Task 6: Fully editable workspace

**Files:**
- Modify: `src/features/trip/travel-board.tsx`, `src/app/globals.css`
- Create: `src/features/trip/preferences-editor.tsx`, `candidate-editor.tsx`, `itinerary-editor.tsx`, `budget-editor.tsx`, `save-status.tsx`
- Test: `src/features/trip/travel-board.test.tsx`

**Interfaces:**
- Consumes canonical/optimistic Trip plus mutation commands.
- Produces accessible preference editing, candidate focus/search, itinerary add/edit/delete/reorder, budget editing, and conflict recovery UI.

- [ ] Write failing interaction tests for every edit surface, optimistic status, delete confirmation, conflict actions, and keyboard ordering.
- [ ] Run focused tests and verify controls are absent.
- [ ] Build focused editor components and wire mutations without local canonical state.
- [ ] Add source badges, inline validation, save/error/conflict styling, and accessible keyboard controls.
- [ ] Run component tests, layout regression, typecheck, and lint.

### Task 7: Migration, restart persistence, and final verification

**Files:**
- Modify: `README.md`, `.env.example`, `package.json`

**Interfaces:**
- Documents DB location, migration, development, reset, testing, and API-key setup.

- [ ] Run migrations on a clean temporary path, create a trip, reopen the database, and verify persistence.
- [ ] Run `npm test`, `npm run typecheck`, `npm run lint`, `npm run build`, and `npm audit --omit=dev`.
- [ ] Start the app and verify browser user edits followed by an agent edit affect the same trip and survive restart.
- [ ] Document commands and report any environment-only verification gap.
