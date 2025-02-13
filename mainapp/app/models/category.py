from sqlalchemy import Column, Integer, String
from core.database import Base


# **SQLAlchemy Modeli (Veritabanı için)**
class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String, nullable=True)
