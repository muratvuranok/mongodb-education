# **Pydantic Modeli (Api için)**
from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    id: int | None = Field(None, description="Kategori Kimliği")
    name: str = Field(
        ...,  # ilgili lan zorunludur
        min_length=3,
        max_length=50,
        description="Kategori Adı an az 3, en fazla 50 karakter olabilir",
        examples=["Elektronik"],
    )
    description: str | None = Field(
        None,
        max_length=255,
        description="Kategori Açıklaması",
        examples=["Elektronik ürünler"],
    )

    class Config:
        from_attributes = (
            True  # Pydantic modelini oluştururken, veritabanı modelinden alanları alır.
        )
        # SQLAlcahemy modelinden dönüşümleri kolaylaştırmak için kullanılır.
