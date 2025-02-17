from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user import UserRequest, UserResponse, LoginRequest
from services.user import (
    get_user_by_username,
    verify_password,
    get_user_by_refrehtoken,
    update_refres_token,
)
from core.auth import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


# **Login**
@router.post(
    "/login", summary="Login", description="Login", response_description="Login"
)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
        
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_access_token(data={"sub": db_user.username})
    update_refres_token(db, db_user.username, refresh_token)

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", summary="Refresh token", description="Refresh token")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    db_user = get_user_by_refrehtoken(db, refresh_token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    new_access_token = create_access_token(data={"sub": db_user.username})

    return {"access_token": new_access_token, "token_type": "bearer"}
