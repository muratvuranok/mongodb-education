from db import category_collection, product_collection
from models.category import Category
from bson.objectid import ObjectId
import json
from bson import json_util
from tabulate import tabulate


class CategoryService:
    """
    Kategori işlemleri için kullanılacak servis sınıfı.
    """
 
    @staticmethod
    def create_category(data):
        """
        Yeni bir kategori oluşturur.

        Args:
            data (dict): Kategori bilgilerini içeren sözlük.
                        Örnek:
                        {
                            "name": "Beverages",
                            "description": "Soft drinks, coffees, teas, beers, and ales"
                        }

        Returns:
            str: Oluşturulan kategori ID'si veya hata mesajı.
        """
        try:
            # Kategori nesnesi oluştur
            category = Category(**data)
            result = category_collection.insert_one(category.to_dict())
            return str(result.inserted_id)
        except Exception as e:
            return f"Kategori oluşturulurken hata oluştu: {str(e)}"

    @staticmethod
    def get_categories():
        """
        Tüm kategorileri getirir.

        Returns:
            list: Tüm kategorileri içeren liste.
        """
        try:
            return list(category_collection.find({}, {"_id": 0}))
        except Exception as e:
            return f"Hata: {str(e)}"

    @staticmethod
    def get_categories_to_table():
        """
        Tüm kategorileri tablo formatında yazdırır.
        """
        try:
            categories = list(category_collection.find({}))
            if not categories:
                print("Kayıtlı kategori bulunamadı.")
                return

            headers = categories[0].keys()  # İlk kategorinin key'lerini al
            rows = [list(category.values()) for category in categories]

            print(tabulate(rows, headers=headers, tablefmt="pretty"))
        except Exception as e:
            print(f"Hata: {str(e)}")

    @staticmethod
    def get_category_by_products(category_id):
        """
        Kategoriye ait ürünleri listeler.

        Args:
            category_id (str): Kategori ObjectId değeri.

        Returns:
            dict: Kategori bilgisi ve ürün listesi.
        """
        try:
            category_id = ObjectId(category_id)
            pipeline = [
                {"$match": {"_id": category_id}},
                {
                    "$lookup": {
                        "from": "Products",
                        "localField": "_id",
                        "foreignField": "category_id",
                        "as": "Products",
                    }
                },
                {"$project": {"_id": 0, "name": 1, "description": 1, "Products": 1}},
            ]
            category_with_products = list(category_collection.aggregate(pipeline))

            if not category_with_products:
                return "Kategori veya ürün bulunamadı."

            return json.dumps(
                category_with_products, indent=4, default=json_util.default
            )
        except Exception as e:
            return f"Hata: {str(e)}"

        # @staticmethod
        # def get_category_by_products(id):
        #     """
        #     Kategori ve ürünleri listeler
        #     """

        #     try:
        #         category_id: ObjectId = ObjectId(id)
        #         pipeline = [
        #             {
        #                 "$match": {"_id": category_id},
        #             },
        #             {
        #                 "$lookup": {
        #                     "from": "Products",
        #                     "let": {
        #                         "category_id": {"$toString": "$_id"}
        #                     },  # kategori sınıfı içerisinde yer alan _id değişkenini string'e çevirip category_id değişkenine atıryoruz.
        #                     "pipeline": [
        #                         {
        #                             "$match": {
        #                                 "$expr": {
        #                                     "$eq": ["$CategoryId", "$$category_id"]
        #                                 }  # products içerisinde yer alan CategoryId değeri ile category_id değerini karşılaştırıyoruz.
        #                             },
        #                         },
        #                         {
        #                             "$project": {
        #                                 "_id": 0,
        #                             }
        #                         },
        #                     ],
        #                     "as": "Products",
        #                 }
        #             },
        #         ]
        #         category_with_products = list(category_collection.aggregate(pipeline))
        #         print(
        #             json.dumps(
        #                 {"category": category_with_products},
        #                 indent=4,
        #                 default=json_util.default,
        #             )
        #         )
        #     except:
        #         pass

        # categoryId ObjectId ise çalışır
        # category_with_products = list(
        #     category_collection.aggregate(
        #         [
        #             {
        #                 "$match": {"_id": ObjectId(id)},
        #             },  # Kategoriyi seçiyoruz.
        #             {
        #                 "$lookup": {
        #                     "from": "products",
        #                     "localField": "_id",
        #                     "foreignField": "CategoryId",
        #                     "as": "Products",
        #                 }
        #             },
        #             {
        #                 "$project": {
        #                     "_id": 0,
        #                     "Name": 1,
        #                     "Description": 1,
        #                     "Products": 1,
        #                 }
        #             },
        #         ]
        #     )
        # )

        # pipeline = [
        #             { "$match": {"_id": ObjectId(id)}, },
        #             {
        #                 "$lookup": {
        #                     "from": "products",
        #                     "let": {"CategoryId": {"$toString": "$_id"}},
        #                     "pipeline":[
        #                         { "$match" : {"$expr": {"$eq":["$CategoryId" , "$$category_id"]}},},
        #                         { "$project": { "_id":0 }  },
        #                     ]
        #                     "localField": "_id",
        #                     "foreignField": "CategoryId",
        #                     "as": "Products"
        #                 }
        #             }
        #         ]

        # category = category_collection.find_one({"_id": ObjectId(id)})
        # if not category:
        #     return None

        # # products = list(product_collection.find({"CategoryId": ObjectId(id)}))
        # products = list(product_collection.find({"CategoryId": id}))
        # return {
        #     "category": category,
        #     "products": products,
        # }

    @staticmethod
    def get_category_by_id(category_id):
        """
        ID değerine göre kategori getirir.

        Args:
            category_id (str): Kategori ObjectId değeri.

        Returns:
            dict: Kategori bilgisi veya hata mesajı.
        """
        try:
            category = category_collection.find_one(
                {"_id": ObjectId(category_id)}, {"_id": 0}
            )
            if not category:
                return "Kategori bulunamadı."
            return category
        except Exception as e:
            return f"Hata: {str(e)}"

    @staticmethod
    def delete_category(category_id):
        """
        ID değerine göre kategori siler.

        Args:
            category_id (str): Silinecek kategori ObjectId değeri.

        Returns:
            str: İşlem sonucu mesajı.
        """
        try:
            category_id = ObjectId(category_id)
            category_collection.delete_one({"_id": category_id})
            product_collection.delete_many(
                {"category_id": category_id}
            )  # Bağlı ürünleri de sil

            return f"Kategori ve bağlı ürünler başarıyla silindi."
        except Exception as e:
            return f"Hata: {str(e)}"
