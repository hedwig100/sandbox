# Trip Library and URL Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make SQLite trips discoverable from a library and directly restorable through stable trip URLs.

**Architecture:** TripService exposes summary listing and cascading deletion. The root page becomes a client library backed by the REST API, while the collaborative workspace moves to a dynamic route whose URL ID is the only trip selector.

**Tech Stack:** Next.js App Router, React, TypeScript, Drizzle ORM, SQLite, Vitest, Testing Library.

## Global Constraints

- `/` lists all local SQLite trips ordered by most recent update.
- `/trips/{tripId}` restores exactly that trip and never silently creates another.
- Creation navigates to the canonical trip URL.
- Deletion requires two deliberate actions and cascades related records.
- Local storage is removed as canonical navigation state.

---

### Task 1: Trip summaries and cascading deletion

**Files:** Modify `src/features/trip/types.ts`, `src/server/trips/service.ts`, `src/server/trips/service.test.ts`.

**Interfaces:** Produce `TripSummary`, `listTrips(): TripSummary[]`, and `deleteTrip(id): void`.

- [ ] Add failing service tests for descending update order, derived summary values, missing deletion, and child-row cascades.
- [ ] Run focused tests and confirm missing methods fail.
- [ ] Implement summary query and transactional deletion.
- [ ] Run focused tests and typecheck.

### Task 2: List and delete REST boundaries

**Files:** Modify `src/app/api/trips/route.ts`, `src/app/api/trips/[tripId]/route.ts`.

**Interfaces:** `GET /api/trips` returns summaries; `DELETE /api/trips/:id` returns 204 or typed 404.

- [ ] Add failing handler tests for list ordering and delete semantics.
- [ ] Implement thin service-backed handlers.
- [ ] Run route/service tests and typecheck.

### Task 3: URL-scoped workspace

**Files:** Modify `src/features/trip/use-trip.ts`; move workspace from `src/app/page.tsx` to `src/app/trips/[tripId]/page.tsx`; create `src/features/trip/trip-workspace.tsx`.

**Interfaces:** `useTrip(tripId)` fetches only the requested trip and exposes a not-found state.

- [ ] Add failing hook tests for requested-ID fetch and 404 without implicit creation.
- [ ] Implement URL-driven hook and workspace component.
- [ ] Compose dynamic route and verify existing chat/edit integration.

### Task 4: Trip library UI

**Files:** Create `src/features/trip/trip-library.tsx`, test; replace `src/app/page.tsx`; modify `src/app/globals.css`.

**Interfaces:** Library fetches summaries, creates and routes to a trip, opens cards, and confirms deletion inline.

- [ ] Add failing UI tests for empty/list/create/error/delete confirmation.
- [ ] Implement library states and accessible navigation.
- [ ] Add responsive editorial card styling and remove legacy local-storage ID.

### Task 5: Verification

**Files:** Modify `README.md`.

- [ ] Verify create, list, direct URL, restart restoration, deletion, and unknown ID on the real server.
- [ ] Run full tests, typecheck, lint, build, and production dependency audit.
- [ ] Keep changes uncommitted and report verification evidence.
