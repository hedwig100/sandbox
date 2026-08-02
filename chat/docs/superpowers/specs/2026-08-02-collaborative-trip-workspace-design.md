# Collaborative Trip Workspace Design

## Goal

Transform Tabi Canvas from a client-owned visualization into a persistent collaborative workspace. The user and the OpenAI agent must be able to perform the same trip operations through one validated backend domain service, with SQLite as the canonical state.

## Product experience

The left pane remains a conversational travel agent. The right pane becomes a fully editable trip workspace rather than a read-only projection. A user can edit trip preferences, choose destinations, create and edit itinerary entries, move entries within and between days, delete entries, and update budget categories. Agent tool calls perform the equivalent operations against the same stored trip.

The interface distinguishes user-authored and agent-authored candidates and itinerary entries. Every edit exposes saving, saved, failed, or conflicted status without blocking unrelated controls. Sample catalog prices remain clearly labeled as illustrative rather than live availability.

## Architecture

SQLite becomes the source of truth. The browser no longer owns canonical `TripState`, and agent tools no longer emit client-only reducer patches.

```text
Editable travel board -> REST route -> TripService -> SQLite
                                      ^
Agent function tools -----------------+

TripService result -> canonical Trip response -> travel board
```

The system has five boundaries:

1. **REST routes** validate HTTP requests, map domain errors to status codes, and serialize canonical trip responses.
2. **Agent tools** validate model arguments and call the same `TripService` methods used by REST routes. They do not make loopback HTTP requests.
3. **TripService** owns all domain rules, authorization-free trip scoping, transactions, version checks, ordering, and catalog operations.
4. **Repository** contains Drizzle queries and maps normalized SQLite rows to domain objects.
5. **Trip workspace client** performs optimistic edits, reconciles canonical responses, and displays save/conflict states.

Neither REST handlers nor agent tools issue SQL directly. The client never writes SQLite directly, and the agent never produces arbitrary UI events.

## Technology and storage

- Next.js App Router and TypeScript
- Drizzle ORM with a local SQLite driver
- Drizzle migrations checked into the repository
- A runtime SQLite database file excluded from Git
- Zod schemas shared at REST, agent-tool, and domain boundaries where appropriate
- OpenAI Responses API for the existing tool loop

The first browser visit creates a trip with `POST /api/trips`. Its ID is stored locally and included in the page URL or browser storage so a refresh restores the same trip. If the stored ID no longer exists, the client creates a new trip and replaces the stale ID.

## Data model

### `trips`

- `id`: text primary key
- `destination`: nullable text
- `start_date`, `end_date`: nullable ISO date text
- `travelers`: positive integer, default 2
- `interests_json`: JSON text containing a string array
- `budget_limit`: nullable positive integer in JPY
- `focused_destination_id`: nullable text
- `version`: positive integer incremented once per successful mutation
- `created_at`, `updated_at`: ISO timestamp text

### `trip_candidates`

- composite key: `trip_id`, `destination_id`
- `source`: `user` or `agent`
- `position`: non-negative integer

### `itinerary_items`

- `id`: text primary key
- `trip_id`: foreign key
- `day`: positive integer
- `position`: non-negative integer within the day
- `time`, `title`, `location`, `note`
- `estimated_cost`: non-negative integer in JPY
- `source`: `user` or `agent`

### `trip_budgets`

- `trip_id`: primary and foreign key
- `transport`, `stay`, `food`, `activities`: non-negative integers in JPY

Trip deletion cascades to candidates, itinerary items, and budget. Creating a trip also creates a zero-valued budget row in one transaction.

## Canonical API representation

Every successful read or mutation returns a complete `Trip` object:

```ts
type Trip = {
  id: string
  version: number
  preferences: {
    destination?: string
    dates?: { start: string; end: string }
    travelers: number
    interests: string[]
    budgetLimit?: number
  }
  candidates: Array<Destination & { source: "user" | "agent"; position: number }>
  focusedDestinationId?: string
  itinerary: Array<ItineraryItem & { source: "user" | "agent"; position: number }>
  budget: Budget
  createdAt: string
  updatedAt: string
}
```

Returning the complete canonical state favors correctness and simple reconciliation over small payloads. The local sample catalog is small, so this is appropriate for the initial release.

## REST API

- `POST /api/trips` creates and returns a trip.
- `GET /api/trips/:tripId` returns the canonical trip.
- `PATCH /api/trips/:tripId/preferences` updates supplied preference fields.
- `POST /api/trips/:tripId/candidates/search` replaces ranked catalog candidates.
- `PATCH /api/trips/:tripId/candidates/:candidateId` selects or clears focus and records user provenance when needed.
- `POST /api/trips/:tripId/itinerary` creates an item.
- `PATCH /api/trips/:tripId/itinerary/:itemId` updates supplied item fields.
- `DELETE /api/trips/:tripId/itinerary/:itemId` removes an item.
- `POST /api/trips/:tripId/itinerary/reorder` atomically changes day and position for all supplied entries.
- `PATCH /api/trips/:tripId/budget` updates supplied budget categories.

Every mutation request includes `version` and `source`. Browser routes force `source` to `user`; agent tools force it to `agent`, regardless of untrusted input. The server validates route IDs against body IDs rather than accepting ambiguous targets.

## Agent tools

The Responses API exposes:

- `get_trip`
- `update_trip_preferences`
- `search_trip_candidates`
- `select_trip_candidate`
- `create_itinerary_item`
- `update_itinerary_item`
- `delete_itinerary_item`
- `reorder_itinerary`
- `update_trip_budget`

The chat request contains `tripId`, not a browser-provided trip snapshot. Before the first model call, the chat route reads the canonical trip. Every mutation tool calls `TripService`, receives an incremented version and complete trip, and uses that version for later calls in the same agent turn. The client receives canonical trip snapshots in the NDJSON stream and replaces its confirmed state.

Tool results include concise mutation summaries plus the resulting version. Full trip state is supplied to the model only when needed to make a subsequent decision, avoiding repeated large tool output.

## User editing behavior

### Preferences

Dates, travelers, interests, destination text, and total budget are editable. Text-like fields use an explicit save action or save on blur; discrete controls save immediately. Invalid values remain local and display inline validation without reaching the API.

### Candidates

Users can select or clear the focused candidate and manually run catalog search with editable interests, season, and daily-cost filters. Source badges distinguish user and agent actions.

### Itinerary

Users can add, edit, and delete entries. Drag and drop changes position within a day or moves an item to another day. A reorder sends the complete ordered list of affected items, and the service normalizes positions to contiguous zero-based values in one transaction.

### Budget

Users can edit each budget category. The workspace displays the category total, configured limit, remaining or exceeded amount, sum of itinerary item estimates, and the difference between itinerary costs and the activities category.

## Optimistic updates and concurrency

The client keeps two layers: the latest confirmed `Trip` and an optimistic presentation derived from pending user operations. An optimistic operation has a stable client ID and enough inverse data to roll itself back.

Every mutation uses compare-and-swap semantics:

```sql
UPDATE trips
SET version = version + 1, updated_at = ?
WHERE id = ? AND version = ?
```

If no row is updated, the service throws a version conflict. The API returns HTTP 409 with the latest canonical trip. The client preserves the user's unsaved form values, renders a conflict notice, and offers “最新状態へ再適用” or “変更を破棄.” It never silently overwrites either side.

Agent execution and user controls may operate concurrently. Unrelated successful updates are reconciled from canonical responses. Updates sharing a stale version receive the same explicit conflict behavior; agent tools report the conflict to the model, which must re-read the trip before retrying.

## Error handling

- Invalid input: HTTP 400 with field-safe validation details.
- Missing trip or item: HTTP 404.
- Stale version: HTTP 409 with latest trip.
- SQLite constraint or transaction failure: HTTP 500 with a stable public code; raw SQL and file paths remain server-only.
- Network failure: optimistic user operation rolls back and exposes retry.
- Agent provider failure: trip mutations already committed remain valid; the chat reports partial completion.
- Reorder failure: the full reorder transaction rolls back.
- Missing or corrupt local database: startup surfaces an actionable server configuration error.

## Accessibility

- All form controls have persistent labels and inline error associations.
- Drag and drop has keyboard alternatives: move up, move down, previous day, and next day.
- Save and conflict status uses text and appropriate live regions, not color alone.
- Destructive delete requires a deliberate confirmation control but not a blocking browser dialog.
- Focus remains on the edited control after successful reconciliation.

## Testing and verification

- Repository integration tests run against a temporary SQLite database and real migrations.
- TripService tests cover create/read, every mutation, version increments, 404 cases, stale versions, ordering normalization, transaction rollback, and provenance enforcement.
- Route tests cover request validation and 400/404/409/500 mapping.
- Agent tests verify tools and REST routes produce equivalent canonical state for equivalent commands.
- Client tests cover optimistic success, rollback, conflict preservation and reapply, CRUD controls, budget derivations, and keyboard reordering.
- Existing OpenAI orchestration tests verify tool sequences use the newest returned version.
- Full verification runs tests, TypeScript, ESLint, production build, migration on a clean database, and a real agent turn when a valid API key is available.

## Scope boundaries

The initial collaborative release has no login, access control, multi-user sharing, WebSocket synchronization, external travel data, booking, or payments. SQLite is for local and single-instance deployment. Multi-process production deployment would require moving the repository implementation to a networked database while retaining the TripService interface.

## Completion criteria

The change is complete when a trip survives server restart; every right-panel field and itinerary operation is user-editable; the agent can perform equivalent operations through the same TripService; stale concurrent mutations return a visible conflict rather than overwriting; and all automated verification passes.
