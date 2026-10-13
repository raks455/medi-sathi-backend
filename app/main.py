from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure.database.session import engine, Base
from app.interfaces.api.v1.auth import router as auth_router
from app.interfaces.api.v1.dashboard import router as dashboard_router
from app.infrastructure.database.models.revoked_token import RevokedTokenModel  # noqa
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (for development only)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Medisathi API",
    description="Medisathi Backend - Clean Architecture",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"message": "Medisathi API is running"}