# Agentic Travel Chat Design

## Goal

Build a working chat application in which an OpenAI-powered travel-planning agent selects typed tools during conversation and those tool results visibly update a travel board. The first release should demonstrate the agent/tool/UI loop clearly without requiring authentication, a database, booking integrations, or third-party travel APIs.

## Product concept

The application is an AI travel planner. A user can describe a trip conversationally, for example: “Plan a three-night food-focused trip for two in November under ¥150,000.” The agent can update trip preferences, search a bundled destination catalog, focus a candidate, add itinerary items, and revise the budget. Each tool execution produces a validated UI event; the browser applies those events to the board and shows a compact execution trace in the conversation.

All destination and price information is illustrative sample data. The interface must label it accordingly and must not imply live availability or booking accuracy.

## Technology

- Next.js with the App Router and TypeScript
- React client components for chat and travel-board interaction
- OpenAI Responses API, called only from the Next.js server
- `OPENAI_API_KEY` read from `.env.local` and never exposed to browser code
- Schema validation for every tool input and server response boundary
- A small test stack appropriate to the generated Next.js project

The project is currently empty, so the implementation may establish these conventions without preserving a prior application structure.

## User experience

### Desktop

The screen is divided into two primary panes:

- The left pane contains the conversation, streaming assistant output, collapsible tool activity, starter prompts, errors, and the composer.
- The right pane is the travel board. It contains the current trip preferences, destination candidates, a day-by-day itinerary, and a categorized budget summary.

The visual direction combines a warm editorial travel aesthetic with clear dashboard controls. Loading, selected, focused, and error states must be visually distinct. Tool activity uses human-readable labels such as “条件を更新” and “候補地を検索,” not raw function names.

### Mobile

Chat and travel board use a two-tab layout. State is shared across both tabs, and a tool-driven change may show a small indicator on the inactive board tab.

### Empty state

The empty chat offers several starter prompts that demonstrate different tool combinations. The board shows an inviting placeholder rather than blank panels.

## Architecture

The application has five focused units:

1. **Chat UI** collects messages, renders streamed output and tool activity, and exposes retry behavior.
2. **Chat route** accepts a conversation plus the current trip-state snapshot, invokes OpenAI, and manages the bounded tool loop.
3. **Tool registry** defines tool schemas and implementations. It is the only server unit that converts a model tool call into domain results and UI events.
4. **Trip reducer** applies typed UI events deterministically to client state.
5. **Travel board** renders `TripState` and emits only direct user-interface actions such as selecting a candidate; it does not interpret model output.

```text
Chat UI
  -> Next.js chat route
  -> OpenAI Responses API
  -> validated tool call
  -> tool registry
  -> tool result returned to OpenAI
  -> assistant text + typed UI event stream
  -> trip reducer
  -> travel board
```

The agent never produces JSX, CSS, arbitrary patches, or direct React state mutations. Only allow-listed typed events can change the board.

## Domain state

The client maintains one canonical state object:

```ts
type TripState = {
  preferences: {
    destination?: string
    dates?: { start: string; end: string }
    travelers: number
    interests: string[]
    budgetLimit?: number
  }
  candidates: Destination[]
  focusedDestinationId?: string
  itinerary: ItineraryDay[]
  budget: {
    transport: number
    stay: number
    food: number
    activities: number
  }
}
```

Shared domain types live outside React components so tools, the route, the reducer, and tests use the same contracts.

## Agent tools

The first release exposes five tools:

- `set_trip_preferences`: updates dates, party size, interests, destination hints, and budget limit. It emits `preferences.updated`.
- `search_destinations`: filters and ranks the bundled destination catalog from validated criteria. It emits `candidates.replaced`.
- `focus_destination`: chooses one existing candidate for emphasis. It emits `destination.focused`.
- `add_to_itinerary`: adds a validated activity, location, time block, estimated cost, and day to the itinerary. It emits `itinerary.itemAdded`.
- `update_budget`: sets validated non-negative estimates for transport, accommodation, food, and activities. It emits `budget.updated`.

Tool implementations must be deterministic for a given input and catalog. They return both a concise model-facing result and zero or more client-facing events. Candidate IDs and destination references are checked against known data or the current state.

## Request and streaming flow

1. The browser sends the conversation and current `TripState` snapshot to the chat route.
2. The route validates the request and supplies the model with a concise system instruction, tool definitions, conversation context, and the state snapshot.
3. OpenAI streams output. Tool calls are accumulated until their complete arguments are available.
4. The route validates and executes requested tools, forwards UI events to the browser, and submits tool results back to OpenAI.
5. Steps 3–4 repeat for at most eight tool-call rounds.
6. The final assistant response streams to the chat UI.
7. The browser applies every event in arrival order through the trip reducer.

Each request has an ID. UI events carry stable event IDs so the client can ignore accidental duplicate delivery. While a request is active, the composer prevents duplicate submission.

Conversation and trip state remain in browser memory for the initial release. Refreshing the page starts a new planning session.

## Failure handling

- A missing `OPENAI_API_KEY` returns a typed configuration error and the UI explains where to set it.
- OpenAI network, authorization, rate-limit, and service errors map to safe user-facing messages with retry where appropriate.
- Invalid tool arguments are not executed. The validation error is returned to the model once so it can correct the call within the same bounded loop.
- Unknown destination IDs, invalid dates, negative costs, and itinerary days outside the selected date range are rejected by domain validation.
- The server stops after eight tool-call rounds and returns a controlled limit message.
- If streaming is interrupted, already received text and applied events remain visible. The user may retry the original message.
- A failed request never rolls back or clears the previously valid travel board.
- Raw API keys, stack traces, and full provider payloads are never sent to the client or written into ordinary application logs.

## Accessibility and responsive behavior

- All interactive controls are keyboard reachable and have visible focus states.
- Status updates and assistant streaming use appropriate live regions without announcing every token.
- Color is not the only indicator of selection, loading, tool completion, or failure.
- Reduced-motion preferences are respected.
- The layout remains usable from a narrow mobile viewport through desktop widths.

## Testing and verification

Automated coverage includes:

- Unit tests for every trip-reducer event, including duplicate-event handling.
- Unit tests for each tool’s validation, deterministic result, and emitted event.
- Server tests with a mocked OpenAI client for a direct answer, one tool call, multiple sequential calls, invalid arguments followed by correction, provider failure, and the eight-round limit.
- A primary interaction test covering message submission, visible tool activity, streamed assistant output, and travel-board updates.
- Type checking, linting, tests, and a production build as final verification.

Manual verification includes desktop and mobile layouts, keyboard navigation, API-key-missing behavior, loading and retry states, and a real OpenAI request when a valid local key is available.

## Scope boundaries

The initial release does not include user accounts, database persistence, shared trips, external maps, live search, live pricing, bookings, payments, or multiple specialized agents. These can be added later without changing the central tool-registry and typed-event architecture.

## Completion criteria

The implementation is complete when a locally running user can converse with an actual OpenAI model, observe at least two different model-selected tools in one planning session, and see the travel board update through validated events while all automated verification commands pass.
