from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.src.core.models import models
from app.src.common.config.database import engine
from app.src.core.routers import user, projects, tasks


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_all_tables()
        yield
    finally:
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(projects.router)
app.include_router(tasks.router)