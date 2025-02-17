from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import verify_access_token
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

# **Router tanımlama**
router = APIRouter(prefix="/api/v1/categories", tags=["Category"])


# **GET - Tüm Kategorileri Getir**
@router.get("/", summary="Get All Categories")
def read_categories(
    db: Session = Depends(get_db), token: str = Depends(verify_access_token)
):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    categories = get_categories(db)
    return {
        "data": categories,
        "message": "Categories retrieved successfully",
        "status": 200,
    }


# **GET - Belirli Bir Kategoriyi Getir**
@router.get("/{category_id}", summary="Get a Category by ID")
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return {
        "data": category,
        "message": "Category retrieved successfully",
        "status": 200,
    }


# **POST - Yeni Kategori Ekle**
@router.post("/", summary="Create a new Category")
def create_new_category(category_data: CategoryRequest, db: Session = Depends(get_db)):
    category = create_category(db, category_data)
    return {"data": category, "message": "Category added successfully", "status": 201}


# **PUT - Kategoriyi Güncelle**
@router.put("/{category_id}", summary="Update a Category")
def update_existing_category(
    category_id: int, category_data: CategoryRequest, db: Session = Depends(get_db)
):
    category = update_category(db, category_id, category_data)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return {"data": category, "message": "Category updated successfully", "status": 200}


# **DELETE - Kategoriyi Sil**
@router.delete("/{category_id}", summary="Delete a Category")
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    category = delete_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return {"message": "Category deleted successfully", "status": 200}
