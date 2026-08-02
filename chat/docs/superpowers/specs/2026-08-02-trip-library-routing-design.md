# Trip Library and URL Routing Design

## Goal

Make every persisted trip recoverable without browser local storage by adding a SQLite-backed trip library and stable `/trips/{tripId}` URLs.

## Routes and screens

- `/` is a trip library ordered by most recently updated.
- `/trips/{tripId}` is the existing chat and collaborative workspace scoped to the URL ID.
- An unknown or deleted ID renders a useful not-found state with a link back to the library.

The library displays destination or “行き先未定,” dates, travelers, budget limit, itinerary count, and updated time. Its primary action creates a trip through `POST /api/trips` and navigates to its URL. Each card opens the trip and exposes a deliberate two-step delete control.

## API and service changes

- `TripService.listTrips()` returns lightweight `TripSummary` records ordered by `updated_at DESC`.
- `TripService.deleteTrip(id)` removes the trip; foreign-key cascades remove its candidates, itinerary, and budget.
- `GET /api/trips` returns summaries.
- Existing `POST /api/trips` creates a trip.
- `DELETE /api/trips/:tripId` deletes a trip and returns HTTP 204.

`TripSummary` contains `id`, destination, optional dates, travelers, optional budget limit, itinerary count, and `updatedAt`. The list endpoint does not hydrate catalog candidates or itinerary item details.

## Navigation and restoration

The collaborative workspace receives `tripId` from its dynamic route and calls `GET /api/trips/{tripId}`. It never creates an implicit replacement when that ID is missing. This prevents a mistyped or deleted URL from silently producing unrelated data.

The prior `tabi-trip-id` local-storage entry is treated only as migration context. The library may surface a matching persisted trip naturally through SQLite listing, then removes the legacy entry. All subsequent restoration is URL- and database-based.

The URL can be copied or bookmarked. It resolves from another browser only when that browser reaches the same application instance and SQLite database. This is not internet sharing or access control.

## Errors and deletion

- List failure shows a retryable library error without creating a trip.
- Create failure keeps the user on the library and re-enables the button.
- Delete initially changes the card action to “削除を確定.” A second action performs deletion; cancel or focus loss restores the ordinary action.
- Deleting the currently open trip elsewhere causes its next fetch or mutation to return 404, after which the workspace links back to `/`.
- Unknown IDs render a not-found workspace state rather than redirecting automatically.

## Accessibility

- Trip cards are links with descriptive accessible names.
- Create and delete statuses use live text.
- Delete confirmation is keyboard operable and does not use a blocking browser dialog.
- Focus moves to the library heading after deleting a card.

## Testing

- Repository/service integration tests verify update ordering, summary values, deletion, and cascades.
- Route tests verify list, create, delete, 404, and 204 semantics.
- Library component tests verify empty, populated, creating, error, and delete-confirmation states.
- Workspace tests verify URL-driven retrieval and not-found behavior.
- Existing editing, agent, type, lint, build, security, and restart-persistence checks remain green.

## Completion criteria

A user can close the browser, later open `/`, find every SQLite-persisted trip, open a stable trip URL, bookmark or copy that URL, create another trip, and delete an unwanted trip without relying on local storage.
