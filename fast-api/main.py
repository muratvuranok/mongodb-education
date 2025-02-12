from fastapi import FastAPI
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

@app.get(
    path="/api/v1/categories",
    tags=["Category"],
    summary="Get All Categories",
    description="This endpoint retrieves all categories from the database.",
)
def get_all_categories():
    return {
        "data": categories,
        "message": f"Total Categories Count: {len(categories)}",
        "status": 200,
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
