from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logging_config import setup_logging
from app.routers import query, upsert
from app.services.database import init_db

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="RAG Prototype API", lifespan=lifespan)

app.include_router(upsert.router, prefix="/api")
app.include_router(query.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Prototype API!"}
