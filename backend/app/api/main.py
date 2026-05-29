from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api.routes import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])

from app.api.v1.train import router as train_router
app.include_router(train_router, prefix="/api/v1", tags=["v1"])

# DEMO feature (removable) — see backend/app/api/v1/demo.py header.
from app.api.v1.demo import router as demo_router
app.include_router(demo_router, prefix="/api/v1", tags=["demo"])
