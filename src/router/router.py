"""Main application Router."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse, HTMLResponse, FileResponse, Response


router = APIRouter(
    prefix="/api",
    tags=["api"]
)


@router.get("/health")
async def test():

    """Health check endpoint."""

    return JSONResponse(content={"message": "Accepted"}, status_code=status.HTTP_202_ACCEPTED)