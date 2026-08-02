# Persistent Chat History Design

## Goal

Persist each trip's user and assistant messages plus human-readable agent tool activity in SQLite, restore them on `/trips/{tripId}`, and use server-owned history as the model context.

## Data model

### `chat_messages`

- `id`: text primary key
- `trip_id`: foreign key with cascade delete
- `role`: `user` or `assistant`
- `content`: text with a validated maximum length
- `status`: `pending`, `completed`, or `failed`
- `sequence`: monotonically increasing integer within the trip
- `created_at`, `updated_at`: ISO timestamps

### `tool_activities`

- `id`: text primary key, using the provider call ID where safe
- `trip_id`: foreign key with cascade delete
- `message_id`: foreign key to its assistant message with cascade delete
- `tool_name`: allow-listed internal tool name
- `label`: stable human-readable label
- `status`: `running`, `completed`, or `failed`
- `sequence`: monotonically increasing integer within the assistant attempt
- `created_at`, `completed_at`: ISO timestamps

Only display content and human-facing execution metadata are stored. Tool arguments, raw provider payloads, API keys, stack traces, and hidden reasoning are not persisted.

## Server API

- `GET /api/trips/{tripId}/chat` returns messages oldest-first with nested activities.
- `POST /api/chat` accepts `tripId`, `content`, and optional `retryMessageId`; it no longer accepts browser-owned history.

The chat service owns creation and retrieval. It validates that retry targets are failed assistant messages belonging to the same trip and locates their preceding user message without inserting a duplicate.

## Request lifecycle

For a new message, the server transactionally inserts one completed user message and one pending assistant message with consecutive sequence numbers. For retry, it inserts only a new pending assistant attempt.

Before invoking OpenAI, the server reads completed user and assistant messages for the trip in sequence order. Failed or empty assistant messages are excluded from model context. Tool activities are display history and are not converted into provider tool calls on later requests.

When a tool starts, an activity row is inserted against the pending assistant message. Completion or validation failure updates the same row. Trip mutations remain committed independently, as in the existing tool architecture.

When final text arrives, the server saves the assistant content and marks it completed before emitting `response.completed`. Provider, tool-limit, or unexpected failure marks the assistant and any running activities failed before emitting the safe error event.

If the browser connection closes after processing begins, server persistence continues for the provider operation where the runtime permits it. A pending record left by process termination is treated as failed during the next history read, preventing a permanent loading state.

## Client behavior

The chat hook loads history when its trip changes and renders it before accepting input. Persisted activities appear beneath their assistant attempt. Completed activities are collapsed by default; failed attempts and activities are visually explicit.

Stream events use database message and activity IDs. Client state updates the same records rather than generating temporary IDs. The message composer sends only the new content and trip ID.

Failed assistant messages expose retry. Retry sends the failed assistant ID, preserves the failed attempt in history, and appends a new assistant attempt without duplicating the user message.

Messages display creation time. Initial restoration scrolls to the newest message; subsequent streamed updates retain the existing auto-scroll behavior.

## Errors and boundaries

- Missing trip or cross-trip retry target: 404.
- Invalid/oversized content or invalid retry state: 400.
- Provider failure: assistant and running activities become failed; committed trip mutations remain.
- History read failure: chat shows retry without affecting the editable trip board.
- A trip deletion cascades through all messages and activities.
- Concurrent sends for one trip obtain unique sequence numbers inside a SQLite transaction.

## Testing

- Temporary-SQLite tests cover ordered persistence, nesting activities, restart restoration, pending recovery, retry without duplicate user message, cross-trip rejection, and trip-delete cascades.
- Chat route tests verify server-owned history input, message IDs in stream events, final completion persistence, and provider/tool failure persistence.
- Client tests verify load, timestamps, nested activity rendering, stream reconciliation, failed state, and retry payload.
- Full tests, typecheck, lint, production build, dependency audit, and one real two-turn OpenAI conversation remain required.

## Scope

The first release does not add message deletion, conversation reset, branching, search, pagination, token summarization, exports, or multi-user access. The complete local history is sent as context; a later iteration must add summarization before histories become large.

## Completion criteria

A user can exchange messages and tools, close the browser, reopen the trip URL, see messages and tool history in order, continue with context preserved, retry a failed response without duplicating the user message, and delete the trip with all chat records cascading.
