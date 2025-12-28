from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.connection import init_db
from src.router import user_router, event_router, candidate_router, attendance_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Event Management API", lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(event_router.router)
app.include_router(candidate_router.router)
app.include_router(attendance_router.router)


@app.get("/")
async def root():
    return {"message": "Event Management API"}
