from fastapi import APIRouter, Depends, HTTPException, status
from core.auth import verify_access_token


router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/")
def protected_route(current_user: dict = Depends(verify_access_token)):
    return {
        "message": "You are authorized",
        "user": current_user["sub"],
    }
