"""
Main application module for the FastAPI RESTful API.

- Sets up the FastAPI app with metadata (title, description, version).
- Defines the lifespan event handler for app startup/shutdown database connections.
- Includes API routers for users and health endpoints.

This serves as the entry point for running the API server.
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .databases import close_db, create_all_tables
from .routes import health_router, users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield
    close_db()


app = FastAPI(
    lifespan=lifespan,
    title="VoteApp",
    description="Simple app to vote",
    version="0.0.0",
)
app.include_router(health_router)
app.include_router(users_router)


@app.get("/", tags=["Root"], include_in_schema=False)
async def read_root():
    return RedirectResponse(url="/docs", status_code=302)


def run():
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
