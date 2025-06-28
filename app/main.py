"""
Main application module for the FastAPI RESTful API.

- Sets up the FastAPI app with metadata (title, description, version).
- Defines the lifespan event handler for app startup/shutdown database connections.
- Includes API routers for users and health endpoints.
- Configures CORS middleware to allow requests from the frontend host.

This serves as the entry point for running the API server.
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .config import config
from .databases import close_db, create_all_tables
from .routes import health_router, users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield
    close_db()


app = FastAPI(
    lifespan=lifespan,
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description=config.APP_DESCRIPTION,
)

app.include_router(health_router)
app.include_router(users_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.FRONTEND_HOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"], include_in_schema=False)
async def read_root():
    return RedirectResponse(url="/docs", status_code=302)


def run():
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
