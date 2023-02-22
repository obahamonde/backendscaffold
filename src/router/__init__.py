"""Routers and related"""

from fastapi.staticfiles import StaticFiles

from fastapi import APIRouter, status

from fastapi.responses import JSONResponse

from src.router.storage import app as storage_router

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/")
async def root_endpoint():
    """Root endpoint."""

    return JSONResponse(
        content={"message": "Welcome to Riders API"}, status_code=status.HTTP_200_OK
    )


@router.get("/health")
async def healthcheck_endpoint():
    """Health check endpoint."""

    return JSONResponse(
        content={"message": "Accepted"}, status_code=status.HTTP_202_ACCEPTED
    )


static = StaticFiles(directory="static", html=True)

router.mount("/static", static, name="static")

router.include_router(storage_router)
