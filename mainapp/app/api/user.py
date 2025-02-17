from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user import UserRequest
from services.user import create_user, get_user_by_username


router = APIRouter(prefix="/user", tags=["User"])


# **Register User**
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    # response_model=UserResponse,
    summary="Register a new user",
    description="Register a new user",
    response_description="User data",
    operation_id="register_user",
    response_model_exclude_none=True,
)
def register_user(user: UserRequest, db: Session = Depends(get_db)):  # -> UserResponse:
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = create_user(db, user)
    return {"message": "User created successfully", "user": new_user}
