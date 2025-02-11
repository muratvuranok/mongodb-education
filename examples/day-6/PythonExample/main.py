from services.category_service import CategoryService
import json
from bson import json_util

# from tabulate import tabulate2


def main():
    while True:
        print("\n Kategori Ürün Yönetim Sistemi")
        print("1 - Kategori Ekle")
        print("2 - Kategori Listesi")
        print("3 - Kategori Listesi - Table")
        print("4 - Kategori Listesi - Products")

        print("0 - Çıkış")

        choise = input("Seçiminiz: ")

        if choise == "1":
            name = input("Kategori Adı: ")
            description = input("Açıklama: ")

            # category_service = CategoryService()
            # category_service.create_category(name, description)

            CategoryService.create_category({"name": name, "description": description})
        elif choise == "2":
            categories = CategoryService.get_categories()
            print("\nKategoriler")
            for category in categories:
                if category["Name"] == None or category["Description"] == None:
                    continue

                print(category["Name"], category["Description"])
        elif choise == "3":
            CategoryService.get_categories_to_table()
        elif choise == "4":
            # id = input("Kategori ID: ")

            id = "67aaf9be3961c0aac69240f5"
            if id == "":
                print("ID boş olamaz")
                continue
            category = CategoryService.get_category_by_products(id)
            # print(category)
            print(
                json.dumps(
                    {
                        "category": category["category"],
                        "products": category["products"] if category else [],
                    },
                    indent=4,
                    default=json_util.default,
                )
            )

        elif choise == "0":
            print("Çıkış yapılıyor...")
        else:
            print("Geçersiz seçim")


if __name__ == "__main__":
    main()
