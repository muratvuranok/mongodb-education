from pydantic import BaseModel, Field


class Category(BaseModel):
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
    
    # existing_categories = ClassVar
