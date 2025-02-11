from db import category_collection, product_collection
from models.category import Category
from bson.objectid import ObjectId
import json
from bson import json_util

# from tabulate import tabulate


class CategoryService:
    """
    Kategori işlemleri için kullanılacak sınıf

    public static string create_category(data){
        // logics
        return data._id.ToString();
    }
    """

    # collection_name = "categories"

    # @staticmethod
    # def create_category(data: Category):
    #     pass

    @staticmethod
    def create_category(data):
        """
        Yeni kategori oluşturur.

        Args:
            data (dict): Kategori bilgilerini içeren sözlük.
                        Örnek:
                        {
                            "Name": "Beverages",
                            "Description": "Soft drinks, coffees, teas, beers, and ales"
                        }

        Returns:
            str: Oluşturulan kategori ID'si.
        """

        category = Category(**data)
        # dict (object)  **data, bu sözlüğün içeriğini Category sınıfının parametrelerine çevirir.
        # category = Category(
        #     data["Name"], data["Description"]
        # )  # dict (object)  **data, bu sözlüğün içeriğini Category sınıfının parametrelerine çevirir.
        # c = Category(data["Name"], data["Description"])

        # result = category_collection.insert_one(data)
        result = category_collection.insert_one(category.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def get_categories():
        """
        Tüm kategorileri getirir.
        {} 1. parantez filtreleme yapılacak alanlar
        {} 2. parantez ise gösterilecek alanlar
        """
        return list(category_collection.find({}, {"_id": 0}))

    @staticmethod
    def get_categories_to_table():
        """
        Tüm kategorileri getirir. Tablo şeklinde gösterir.
        """
        categories = list(category_collection.find({}, {"_id": 0}))
        headers = categories[0].keys()  # İlk kategorinin key'lerini alır
        rows = [list(category.values()) for category in categories]

        # print(tabulate(rows, headers=headers, tablefmt="pretty"))

    @staticmethod
    def get_category_by_products(id):
        """
        Kategori ve ürünleri listeler
        """

        try:
            category_id: ObjectId = ObjectId(id)
            pipeline = [
                {
                    "$match": {"_id": category_id},
                },
                {
                    "$lookup": {
                        "from": "Products",
                        "let": {
                            "category_id": {"$toString": "$_id"}
                        },  # kategori sınıfı içerisinde yer alan _id değişkenini string'e çevirip category_id değişkenine atıryoruz.
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$eq": ["$CategoryId", "$$category_id"]
                                    }  # products içerisinde yer alan CategoryId değeri ile category_id değerini karşılaştırıyoruz.
                                },
                            },
                            {
                                "$project": {
                                    "_id": 0,
                                }
                            },
                        ],
                        "as": "Products",
                    }
                },
            ]
            category_with_products = list(category_collection.aggregate(pipeline))
            print(
                json.dumps(
                    {"category": category_with_products},
                    indent=4,
                    default=json_util.default,
                )
            )
        except:
            pass

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

        category = category_collection.find_one({"_id": ObjectId(id)})
        if not category:
            return None

        # products = list(product_collection.find({"CategoryId": ObjectId(id)}))
        products = list(product_collection.find({"CategoryId": id}))
        return {
            "category": category,
            "products": products,
        }

    @staticmethod
    def get_category_by_id(id):
        """
        ID değerine göre kategori getirir
        """
        try:
            category = category_collection.find_one({"_id": ObjectId(id)}, {"_id": 0})
            # kategoriye ait ürünler listelenir, kategori ile birlikte bir model olarak geriye döndrilebilir.
            return category
        except:
            return None

    @staticmethod
    def delete_category(id):
        """
        ID değerine göre kategori siler
        """
        category_collection.delete_one({"_id": ObjectId(id)})
        product_collection.delete_many({"CategoryId": ObjectId(id)})  # cascade
        return True

    # def topla(*args):   # params
    #     """
    #     t = topla(1,2,3,4,5)
    #     return -> 15
    #     """
    #     return sum(args)  # tüm parametreleri toplar

    # def bilgiler(**kwargs):  # keyword params
    #     """
    #     bilgiler(name="Ali", age=25,"city":"Ankara", "country":"Turkey", "phone":"1234567890", "email":"isim@soyisim.com")
    #     return -> {"name": "Ali", "age": 25}
    #     """
    #     return kwargs

    # def bilgiler2(*args, **kwargs):
    #     """
    #     bilgiler2(1,2,3,4,5,6,7,8,9,n, name="", age=25, city="Ankara")

    #     """
    #     pass

    # Category(**data) -> {key: value, key: value} -> (key=value, key=value)
    # ** bilgiler(key=value, key=value) -> {"key": "value", "key": "value"}
