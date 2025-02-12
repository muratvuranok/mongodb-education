from fastapi import FastAPI
from pydantic import BaseModel


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
            "name": "Home",
            "description": "Api documentation and home page.",
        },
        {
            "name": "Items",
            "description": "Operations with items. The **items** endpoint lets you read and write items.",
        },
        {
            "name": "Users",
            "description": "Operations with users. The **users** endpoint lets you read and write users",
        },
        {
            "name": "Category",
            "description": "Operations with category. The **category** endpoint lets you read and write category",
        },
        {
            "name": "Product",
            "description": "Operations with product. The **product** endpoint lets you read and write product",
        },
    ],
    docs_url="/swagger",  # swagger için url tanımlaması /swagger adresinden ulaşabiliriz.
    redoc_url="/api-docs",  # redoc için url tanımlaması /api-doc adresinden ulaşabiliriz.
    openapi_url="/api/v1/openapi.json",  # OpenAPI için url tanımlaması /api/v1/openapi.json adresinden ulaşabiliriz.
)


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


items = []


@app.get(
    path="/",
    tags=["Home"],
    summary="Home page",
    description="This is the home page of the API. You can find the documentation here.",
)
def read_root():
    return {"data": None, "message": "Hello, World!", "status": 200}


@app.get(
    path="/api/v1/items",
    tags=["Items"],
    summary="Retrieve all items",
    description="This endpoint retrieves all items from the database.",
)
def get_items():
    return {"data": items, "message": None, "status": 200}


@app.post(
    path="/api/v1/items",
    tags=["Items"],
    summary="Create an item",
    description="This endpoint creates an item in the database.",
)
def create_items(item: Item):
    items.append(item)
    return {"data": item, "message": "item added successfully", "status": 201}
