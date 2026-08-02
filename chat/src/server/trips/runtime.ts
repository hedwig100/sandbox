import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { createTripService } from "./service";

const path = process.env.TRIP_DB_PATH ?? "data/trips.sqlite";
mkdirSync(dirname(path), { recursive: true });
export const tripService = createTripService(path);
