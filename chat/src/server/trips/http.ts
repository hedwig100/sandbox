import { TripError } from "./errors";

export const jsonError = (error: unknown) => {
  if (error instanceof TripError) return Response.json({ code: error.code, message: error.message, latest: error.latest }, { status: error.code === "NOT_FOUND" ? 404 : error.code === "VERSION_CONFLICT" ? 409 : 400 });
  console.error("Trip API error", error);
  return Response.json({ code: "INTERNAL_ERROR", message: "旅行データの更新に失敗しました。" }, { status: 500 });
};
export const body = async (request: Request) => request.json() as Promise<Record<string, unknown>>;
