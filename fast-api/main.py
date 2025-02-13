from fastapi import FastAPI, Path, Query
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


categories = ["Electronics", "Clothing", "Books", "Home & Kitchen"]

# @app.get(
#     path="/api/v1/categories",
#     tags=["Category"],
#     summary="Get All Categories",
#     description="This endpoint retrieves all categories from the database.",
# )
# def get_all_categories():
#     return {
#         "data": categories,
#         "message": f"Total Categories Count: {len(categories)}",
#         "status": 200,
#     }


@app.get(
    path="/api/v1/categories",
    tags=["Category"],
    summary="Get All Categories",
    description="This endpoint retrieves all categories from the database.",
)
def get_all_categories(
    search: str | None = Query(
        None,
        title="Search",
        description="Search for a category",
        # min_length=3,
        # max_length=50
    )
):
    """
    Query Parametre Kullanımı
    ?search=keyword şeklinde kullanılır.
    """

    if search:
        filtered_categories = [
            category for category in categories if search.lower() in category.lower()
        ]
        return {
            "data": filtered_categories,
            "message": f"Total Categories Count: {len(filtered_categories)}",
            "status": 200,
        }

    return {
        "data": categories,
        "message": f"Total Categories Count: {len(categories)}",
        "status": 200,
    }


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
    )
):
    """
    **Path Parametre Kullanımı:**
    - `/api/v1/categories/1` şeklinde kullanılır.
    """

    if category_id >= len(
        categories
    ):  # index üzerinden işlem yaptığımız için = kullandık
        return {
            "message": "Category not found",
            "data": None,
            "status": 404,
        }

    return {
        "data": categories[category_id],
        "message": "Category added successfully",
        "status": 201,
    }


@app.post(
    path="/api/v1/categories",
    tags=["Category"],
    summary="Create an item",
    description="This endpoint creates an item in the database.",
)
def create_items(category: Category):
    categories.append(category)
    return {"data": category, "message": "Category added successfully", "status": 201}
