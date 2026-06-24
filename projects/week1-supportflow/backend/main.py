from contextlib import asynccontextmanager

from app.api import tickets
from app.core.config import settings
from app.core.database import init_db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("✅ Database Initialized")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Customer Support Platform",
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(tickets.router, prefix="/api/v1", tags=["tickets"])


@app.get("/")
async def root():
    return {"message": "SupportFlow API is running 🚀"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
