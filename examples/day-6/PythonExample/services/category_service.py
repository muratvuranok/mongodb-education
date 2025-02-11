from db import category_colleciton, product_collection
from models.category import Category
from bson.objectid import ObjectId


class CategoryService:
    """
    Kategori işlemleri için kullanılacak sınıf
    """

    collection_name = "categories"

    def create_category(data):
        """
        Yeni kategori oluşturur
        {
            "Name": "Beverages",
            "Description": "Soft drinks, coffees, teas, beers, and ales"
        }
        """
        category = Category(
            **data
        )  # dict (object)  **data, bu sözlüğün içeriğini Category sınıfının parametrelerine çevirir.
        # c = Category(data["Name"], data["Description"])

        result = category_colleciton.insert_one(category.to_dict())
        return str(result.inserted_id)

    def get_categories():
        """
        Tüm kategorileri getirir.
        {} 1. parantez filtreleme yapılacak alanlar
        {} 2. parantez ise gösterilecek alanlar
        """
        return list(category_colleciton.find({}, {"_id": 0}))

    def get_category_by_products(id):
        """
        Kategori ve ürünleri listeler
        """
        category = category_colleciton.find_one({"_id": ObjectId(id)})
        if not category:
            return None

        products = list(
            product_collection.find(
                {"CategoryId": ObjectId(category["_id"])}, {"_id": 0}
            )
        )
        return {"category": category, "products": products}

    def get_category_by_id(id):
        """
        ID değerine göre kategori getirir
        """
        try:
            category = category_colleciton.find_one({"_id": ObjectId(id)}, {"_id": 0})
            return category
        except:
            return None

    def delete_category(id):
        """
        ID değerine göre kategori siler
        """
        category_colleciton.delete_one({"_id": ObjectId(id)})
        product_collection.delete_many({"CategoryId": ObjectId(id)})  # cascade
        return True
