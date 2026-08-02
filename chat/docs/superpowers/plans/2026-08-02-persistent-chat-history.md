# Persistent Chat History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist trip-scoped messages and tool activity in SQLite, restore them on direct URLs, and continue model context from server-owned history.

**Architecture:** A ChatService owns message/activity sequencing and lifecycle transitions. The chat route receives only new content or a retry target, loads model context from ChatService, and emits database IDs; the client loads and reconciles that canonical history.

**Tech Stack:** Next.js, TypeScript, Drizzle ORM, SQLite, OpenAI Responses API, React, Vitest.

## Global Constraints

- Messages and human-readable activity metadata persist per trip.
- Raw tool arguments, provider payloads, API keys, stack traces, and reasoning are never stored.
- Failed retries do not duplicate user messages.
- Trip deletion cascades chat records.
- Browser history is not trusted as model context.

---

### Task 1: Schema and ChatService

**Files:** Modify DB schema, migration, DDL, shared types; create `src/server/chat/service.ts` and tests.

- [ ] Write failing temporary-SQLite tests for ordered messages, nested activities, lifecycle completion/failure, retry, restart, and cascade.
- [ ] Add chat tables and implement transactional ChatService operations.
- [ ] Run focused tests and typecheck.

### Task 2: History API and persistent chat route

**Files:** Create `/api/trips/[tripId]/chat`; modify `/api/chat` and stream types.

- [ ] Add failing route/service-boundary tests for history retrieval and retry validation.
- [ ] Make POST chat accept `{tripId, content, retryMessageId?}` and load provider context from SQLite.
- [ ] Persist tool activity and final/failed assistant state; stream database IDs.

### Task 3: Restoration and retry client

**Files:** Modify chat hook and panel; add focused tests/styles.

- [ ] Add failing tests for restored history, timestamps, nested activities, failed attempts, and retry payload.
- [ ] Load canonical history by trip, reconcile stream IDs, and expose retry per failed assistant attempt.
- [ ] Render persisted tool histories and timestamps accessibly.

### Task 4: Verification

- [ ] Verify a real two-turn conversation, browser/API reload, server restart, retry state, and trip deletion cascade.
- [ ] Run all tests, typecheck, lint, build, and production dependency audit.
- [ ] Keep all work uncommitted.
