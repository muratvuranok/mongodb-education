from fastapi import FastAPI
from core.config import settings
from api.category import router as category_router
from api.auth import router as auth_router
from api.protected import router as protected_router
from api.user import router as user_router
from api.cache import router as cache_router

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
            "name": "Authentication",
            "description": "Operations with authentication. The **auth** endpoint lets you authenticate users",
        },
        {
            "name": "Protected",
            "description": "Operations with protected. The **protected** endpoint lets you access protected routes",
        },
        {
            "name": "User",
            "description": "Operations with user. The **user** endpoint lets you read and write user",
        },
        {
            "name": "Cache",
            "description": "Operations with cache. The **cache** endpoint lets you read and write cache",
        },
    ],
    docs_url="/swagger",
    redoc_url="/api-docs",
    openapi_url="/api/v1/openapi.json",
)

app.include_router(category_router)
app.include_router(protected_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(cache_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)
