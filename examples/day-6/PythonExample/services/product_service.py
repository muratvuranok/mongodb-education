from db import product_collection, category_collection
from models.product import Product
from bson.objectid import ObjectId
import json
from bson import json_util
from tabulate import tabulate


class ProductService:
    """
    Ürün işlemleri için servis sınıfı.
    """

    @staticmethod
    def create_product(data):
        """
        Yeni bir ürün oluşturur.

        Args:
            data (dict): Ürün bilgilerini içeren sözlük.
                        Örnek:
                        {
                            "name": "Chai",
                            "price": 10.5,
                            "units_in_stock": 100,
                            "category_id": "67aaf9be3961c0aac69240f5"
                        }

        Returns:
            str: Oluşturulan ürün ID'si veya hata mesajı.
        """
        try:
            # Kategori kontrolü
            category_id = data.get("category_id", None)
            if not category_collection.find_one({"_id": ObjectId(category_id)}):
                return "Geçersiz kategori ID'si!"

            # Ürün nesnesi oluştur
            product = Product(**data)
            result = product_collection.insert_one(product.to_dict())
            return f"Ürün eklendi! ID: {result.inserted_id}"
        except Exception as e:
            return f"Hata: {str(e)}"

    @staticmethod
    def get_products():
        """
        Tüm ürünleri getirir.

        Returns:
            list: Ürünleri içeren liste.
        """
        try:
            products = list(product_collection.find({}))
            return json.dumps(products, indent=4, default=json_util.default)
        except Exception as e:
            return f"Hata: {str(e)}"

    @staticmethod
    def get_products_to_table():
        """
        Ürünleri tablo formatında gösterir.
        """
        try:
            products = list(product_collection.find({}, {"_id": 0}))
            if not products:
                print("Ürün bulunamadı.")
                return

            headers = products[0].keys()
            rows = [list(product.values()) for product in products]

            print(tabulate(rows, headers=headers, tablefmt="pretty"))
        except Exception as e:
            print(f"Hata: {str(e)}")

    @staticmethod
    def get_product_by_id(product_id):
        """
        ID'ye göre bir ürünü getirir.

        Args:
            product_id (str): Ürün ID.

        Returns:
            dict: Ürün bilgisi veya hata mesajı.
        """
        try:
            product = product_collection.find_one(
                {"_id": ObjectId(product_id)}, {"_id": 0}
            )
            if not product:
                return "Ürün bulunamadı."
            return product
        except Exception as e:
            return f"Hata: {str(e)}"

    @staticmethod
    def update_product(product_id, update_data):
        """
        Belirtilen ürünün bilgilerini günceller.

        Args:
            product_id (str): Güncellenecek ürünün ObjectId değeri.
            update_data (dict): Güncellenecek alanlar.

        Returns:
            str: Güncelleme sonucu mesajı.
        """
        try:
            result = product_collection.update_one(
                {"_id": ObjectId(product_id)}, {"$set": update_data}
            )
            if result.modified_count == 0:
                return "Ürün bulunamadı veya güncelleme yapılmadı."
            return "Ürün başarıyla güncellendi."
        except Exception as e:
            return f"Hata: {str(e)}"

    @staticmethod
    def delete_product(product_id):
        """
        ID'ye göre ürünü siler.

        Args:
            product_id (str): Silinecek ürünün ObjectId değeri.

        Returns:
            str: Silme işleminin sonucu.
        """
        try:
            result = product_collection.delete_one({"_id": ObjectId(product_id)})
            if result.deleted_count == 0:
                return "Ürün bulunamadı."
            return "Ürün başarıyla silindi."
        except Exception as e:
            return f"Hata: {str(e)}"

    @staticmethod
    def get_products_by_category(category_id):
        """
        Belirtilen kategoriye ait ürünleri getirir.

        Args:
            category_id (str): Kategori ObjectId.

        Returns:
            list: Kategoriye ait ürünlerin listesi.
        """
        try:
            products = list(
                product_collection.find({"category_id": ObjectId(category_id)})
            )
            if not products:
                return "Bu kategoriye ait ürün bulunamadı."
            return json.dumps(products, indent=4, default=json_util.default)
        except Exception as e:
            return f"Hata: {str(e)}"
