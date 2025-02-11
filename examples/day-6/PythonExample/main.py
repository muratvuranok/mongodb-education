from services.category_service import CategoryService
from services.product_service import ProductService
import json
from bson import json_util


def main():
    while True:
        print("\nKategori ve Ürün Yönetim Sistemi")
        print("1 - Kategori Ekle")
        print("2 - Kategori Listesi")
        print("3 - Kategori Listesi (Tablo Formatı)")
        print("4 - Kategori Güncelle")
        print("5 - Kategori Sil")
        print("6 - Belirli Bir Kategoriye Ait Ürünleri Getir")
        print("7 - Ürün Ekle")
        print("8 - Ürün Listesi")
        print("9 - Belirli Bir Kategorinin Ürünlerini Getir")
        print("10 - Ürün Güncelle")
        print("11 - Ürün Sil")
        print("0 - Çıkış")

        choice = input("\nSeçiminiz: ").strip()

        # --- KATEGORİ İŞLEMLERİ ---
        if choice == "1":  # Kategori Ekleme
            name = input("Kategori Adı: ").strip()
            description = input("Açıklama: ").strip()

            if not name or not description:
                print("Kategori adı ve açıklama boş olamaz!")
                continue

            result = CategoryService.create_category({"name": name, "description": description})
            print(f"Kategori eklendi! ID: {result}")

        elif choice == "2":  # Kategori Listesi
            categories = CategoryService.get_categories()
            if categories:
                print("\nKategoriler:")
                for category in categories:
                    print(f"{category['name']} - {category['description']}")
            else:
                print("Kayıtlı kategori bulunamadı!")

        elif choice == "3":  # Kategori Listesi (Tablo Formatı)
            print("\nKategoriler (Tablo Formatı)")
            CategoryService.get_categories_to_table()

        elif choice == "4":  # Kategori Güncelleme
            category_id = input("Güncellenecek Kategori ID: ").strip()

            if not category_id:
                print("Kategori ID boş olamaz!")
                continue

            print("Güncellenecek alanları boş bırakabilirsiniz.")
            name = input("Yeni Kategori Adı: ").strip()
            description = input("Yeni Açıklama: ").strip()

            update_data = {}

            if name:
                update_data["name"] = name
            if description:
                update_data["description"] = description

            if not update_data:
                print("Güncellemek için en az bir alan doldurulmalıdır!")
                continue

            result = CategoryService.update_category(category_id, update_data)
            print(result)

        elif choice == "5":  # Kategori Silme
            category_id = input("Silinecek Kategori ID: ").strip()

            if not category_id:
                print("Kategori ID boş olamaz!")
                continue

            result = CategoryService.delete_category(category_id)
            print(result)

        elif choice == "6":  # Belirli Bir Kategorinin Ürünlerini Getirme
            category_id = input("Kategori ID: ").strip()

            if not category_id:
                print("ID boş olamaz!")
                continue

            category = CategoryService.get_category_by_products(category_id)

            if isinstance(category, str):
                print(category)
            else:
                print("\nKategori ve Ürünler")
                print(
                    json.dumps(
                        {
                            "category": category.get("category", {}),
                            "products": category.get("products", []),
                        },
                        indent=4,
                        default=json_util.default,
                    )
                )

        # --- ÜRÜN İŞLEMLERİ ---
        elif choice == "7":  # Ürün Ekleme
            name = input("Ürün Adı: ").strip()
            price = input("Fiyat: ").strip()
            units_in_stock = input("Stok Miktarı: ").strip()
            category_id = input("Kategori ID: ").strip()

            if not name or not price or not units_in_stock or not category_id:
                print("Ürün bilgileri eksik olamaz!")
                continue

            try:
                price = float(price)
                units_in_stock = int(units_in_stock)
            except ValueError:
                print("Fiyat ve stok miktarı sayısal olmalıdır!")
                continue

            result = ProductService.create_product(
                {
                    "name": name,
                    "price": price,
                    "units_in_stock": units_in_stock,
                    "category_id": category_id,
                }
            )
            print(result)

        elif choice == "8":  # Tüm Ürünleri Listeleme
            print("\nÜrünler:")
            print(ProductService.get_products())

        elif choice == "9":  # Belirli Kategorinin Ürünlerini Getirme
            category_id = input("Kategori ID: ").strip()

            if not category_id:
                print("Kategori ID boş olamaz!")
                continue

            products = ProductService.get_products_by_category(category_id)
            print(products)

        elif choice == "10":  # Ürün Güncelleme
            product_id = input("Güncellenecek Ürün ID: ").strip()

            if not product_id:
                print("Ürün ID boş olamaz!")
                continue

            print("Güncellenecek alanları boş bırakabilirsiniz.")
            name = input("Yeni Ürün Adı: ").strip()
            price = input("Yeni Fiyat: ").strip()
            units_in_stock = input("Yeni Stok Miktarı: ").strip()

            update_data = {}

            if name:
                update_data["name"] = name
            if price:
                try:
                    update_data["price"] = float(price)
                except ValueError:
                    print("Fiyat sayısal olmalıdır!")
                    continue
            if units_in_stock:
                try:
                    update_data["units_in_stock"] = int(units_in_stock)
                except ValueError:
                    print("Stok miktarı sayısal olmalıdır!")
                    continue

            if not update_data:
                print("Güncellemek için en az bir alan doldurulmalıdır!")
                continue

            result = ProductService.update_product(product_id, update_data)
            print(result)

        elif choice == "11":  # Ürün Silme
            product_id = input("Silinecek Ürün ID: ").strip()

            if not product_id:
                print("Ürün ID boş olamaz!")
                continue

            result = ProductService.delete_product(product_id)
            print(result)

        elif choice == "0":  # Çıkış
            print("Çıkış yapılıyor...")
            break  # Sonsuz döngü engellendi

        else:
            print("Geçersiz seçim! Lütfen 0-11 arasında bir değer giriniz.")


if __name__ == "__main__":
    main()
