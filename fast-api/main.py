from typing import List
from fastapi import FastAPI, Path, Query, Depends, HTTPException, status
from models.category import Category

app = FastAPI(
    title="FastAPI Example",
    description="This API allows you to perform CRUD operations on items.",
    version="1.0.0",
    contact={
        "name": "John Doe",
        "url": "https://example.com/contact",
        "email": "isim@soyisim.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=[
        {
            "name": "Category",
            "description": "Operations with category. The **category** endpoint lets you read and write category",
        },
        {
            "name": "Product",
            "description": "Operations with product. The **product** endpoint lets you read and write product",
        },
    ],
    docs_url="/swagger",
    redoc_url="/api-docs",
    openapi_url="/api/v1/openapi.json",
)

# dbcollection
categories = ["Electronics", "Clothing", "Books", "Home & Kitchen", "Music"]


def get_db():
    db = categories
    try:
        yield db
    finally:
        pass


@app.get(
    path="/api/v1/categories",
    tags=["Category"],
    summary="Get All Categories",
    description="This endpoint retrieves all categories from the database.",
)
def get_all_categories(
    search: str | None = Query(
        None, title="Search", description="Search for a category"
    ),
    db: List[str] = Depends(get_db),
):
    """
    Query Parametre Kullanımı
    ?search=keyword şeklinde kullanılır.


    **Dependenct Injection Kullanımı**
    - `Depends(get_db)` şeklinde kullanılır. veri taban bağlantısını bağımlılık olarak inject eder.
    - `db` paramtresi `get_db` fonksiyonundan dönen veriyi alır.
    """

    if search:
        filtered_categories = [
            category for category in db if search.lower() in category.lower()
        ]
        return {
            "data": filtered_categories,
            "message": f"Total Categories Count: {len(filtered_categories)}",
            "status": status.HTTP_200_OK,
        }

    return {
        "data": categories,
        "message": f"Total Categories Count: {len(categories)}",
        "status": status.HTTP_200_OK,
    }


# **Özel HTTP Hata Tanımlama**
def category_not_found_exeption():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": "Category not found",
            "data": None,
            "status": status.HTTP_404_NOT_FOUND,
        },
        headers={"X-Error": "There goes my error"},
    )


@app.get(
    path="/api/v1/categories/{category_id}",
    tags=["Category"],
    summary="Get a Category",
    description="This endpoint retrieves a category from the database.",
)
def get_category_by_id(
    category_id: int = Path(
        ...,  # zorunlu alan
        title="Category ID",
        description="Category ID is required",
        gte=0,  # greater than or equal (0'dan büyük veya eşit olmalı)
        # gt=0,  # greater than ( 0'dan büyük olmalı)
        # lt=5,  # less than (5'ten küçük olmalı)
    ),
    db: List[str] = Depends(get_db),
):
    """
    **Path Parametre Kullanımı:**
    - `/api/v1/categories/1` şeklinde kullanılır.
    """

    if category_id >= len(db):  # index üzerinden işlem yaptığımız için = kullandık
        # return {
        #     "message": "Category not found",
        #     "data": None,
        #     "status": 404,
        # }
        category_not_found_exeption()

    return {
        "data": db[category_id],
        "message": "Category retrieved successfully",
        "status": status.HTTP_200_OK,
    }


@app.post(
    path="/api/v1/categories",
    tags=["Category"],
    summary="Create an item",
    description="This endpoint creates an item in the database.",
)
def create_items(
    category: Category,
    db: List[str] = Depends(get_db),
):
    db.append(category)
    return {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": {
            "data": category,
            "message": "Category added successfully",
            "status": status.HTTP_201_CREATED,
        },
        "headers": {"X-Error": "There goes my error"},
    }
