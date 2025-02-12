from fastapi import FastAPI
# Pydantic is a data validation library in Python. It is used to validate the data sent to the server by the client.
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str  # = "test product"
    description: str | None = (
        None  # ürün açıklaması boş geçilebilir. (isteğe bağlı, var sayılan olarak None değeri atanmıştır.)
    )
    price: float


items = []


@app.get("/")
def read_root():
    return {"data": None, "message": "Hello, World!", "status": 200}


@app.get("/api/v1/items")
def get_items():
    return {"data": items, "message": None, "status": 200}


@app.post("/api/v1/items")
def create_items(item: Item):
    items.append(item)
    return {"data": item, "message": "item added successfully", "status": 201}



# api documentation
# swagger -> http://127.0.0.1:8000/docs
# redoc   -> http://127.0.0.1:8000/redoc


# class Category:  # base -> super -> parent class

#     Name: str = None
#     Description: str = None

#     def __init__(self, name=None, description=None):  # record
#         self.Name = name
#         self.Description = description


# c = Category(description="Test descr")
# c.Name = "Test"
# c.Description = "Test Description"
