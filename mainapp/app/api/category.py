from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from services.category import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category,
)
from models.category import CategoryModel
from schemas.category import CategoryRequest
from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel


class HeadersEnum(str, Enum):
    SUCCESS = ("X-Success",)
    ERROR = ("X-Error",)
    WARNING = "X-Warning"


class GenericResponse:
    status_code: int
    detail: Dict[str, Any]  # string, dynamic
    headers: Dict[Any, str] #{}


router = APIRouter(
    prefix="/categories",
    tags=["Category"],
)


# **GET - Get all categories**
@router.get("/", summary="Get all categories", status_code=status.HTTP_201_CREATED,)
def read_categories(db: Session = Depends(get_db)):
    categories = get_categories(db)
    # return GenericResponse(
    #     status_code=status.HTTP_200_OK,
    #     detail={
    #         "data": categories,
    #         "message": "Categories retrieved successfully",
    #     },
    #     headers={
    #         HeadersEnum.SUCCESS: "Successfully retrieved categories",
    #     },
    # )

    return {
        "status_code": status.HTTP_200_OK,
        "detail": {
            "data": categories,
            "message": "Categories retrieved successfully",
        },
        "headers": {"X-Success": "Successfully retrieved categories"},
    }


# **GET - Get Category**


# **POST - Create a new Category**
@router.post(
    "/",
    summary="Create a new category",
    status_code=status.HTTP_201_CREATED,
)
def create_new_category(request: CategoryRequest, db: Session = Depends(get_db)):
    category = create_category(db, request)
    return category  # generic bir response modeli ekliycez :)
