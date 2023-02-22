from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router import router

__version__ = "0.1.0"


def create_app() -> FastAPI:
    app = FastAPI(
        title="Riders API",
        description="API for Riders",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app
