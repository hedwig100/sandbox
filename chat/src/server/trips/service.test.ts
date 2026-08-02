import { rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { afterEach, describe, expect, it } from "vitest";
import { createTripService } from "./service";

const paths: string[] = [];
afterEach(() => paths.splice(0).forEach((path) => rmSync(path, { force: true })));

describe("TripService", () => {
  it("persists a versioned trip across database connections", () => {
    const path = join(tmpdir(), `tabi-${crypto.randomUUID()}.sqlite`); paths.push(path);
    const first = createTripService(path);
    const created = first.createTrip();
    const updated = first.updatePreferences({ tripId: created.id, version: 1, source: "user", travelers: 3, interests: ["食"] });
    expect(updated.version).toBe(2);
    first.close();

    const reopened = createTripService(path);
    expect(reopened.getTrip(created.id)).toMatchObject({ version: 2, preferences: { travelers: 3, interests: ["食"] } });
    reopened.close();
  });

  it("rejects stale writes with the latest trip", () => {
    const path = join(tmpdir(), `tabi-${crypto.randomUUID()}.sqlite`); paths.push(path);
    const service = createTripService(path); const trip = service.createTrip();
    service.updateBudget({ tripId: trip.id, version: 1, source: "user", food: 12000 });
    expect(() => service.updateBudget({ tripId: trip.id, version: 1, source: "agent", stay: 30000 })).toThrowError(expect.objectContaining({ code: "VERSION_CONFLICT", latest: expect.objectContaining({ version: 2 }) }));
    service.close();
  });

  it("lists newest trips first with summary values", () => {
    const path = join(tmpdir(), `tabi-${crypto.randomUUID()}.sqlite`); paths.push(path);
    const service = createTripService(path); const older = service.createTrip(); const newer = service.createTrip();
    service.updatePreferences({ tripId: older.id, version: 1, source: "user", destination: "京都", travelers: 3, budgetLimit: 90000 });
    service.createItineraryItem({ tripId: older.id, version: 2, source: "user", day: 1, time: "10:00", title: "市場", location: "錦市場", note: "", estimatedCost: 1000 });
    const list = service.listTrips();
    expect(list.map((trip) => trip.id)).toEqual([older.id, newer.id]);
    expect(list[0]).toMatchObject({ destination: "京都", travelers: 3, budgetLimit: 90000, itineraryCount: 1 });
    service.close();
  });

  it("deletes a trip and all child records", () => {
    const path = join(tmpdir(), `tabi-${crypto.randomUUID()}.sqlite`); paths.push(path);
    const service = createTripService(path); const trip = service.createTrip();
    service.searchCandidates({ tripId: trip.id, version: 1, source: "user", interests: ["食"] });
    service.deleteTrip(trip.id);
    expect(service.listTrips()).toEqual([]);
    expect(() => service.getTrip(trip.id)).toThrowError(expect.objectContaining({ code: "NOT_FOUND" }));
    service.close();
  });
});
