from services.category_service import CategoryService


def main():
    while True:
        print("\n Kategori Ürün Yönetim Sistemi")
        print("1 - Kategori Ekle")

        print("0 - Çıkış")

        choise = input("Seçiminiz: ")

        if choise == "1":
            name = input("Kategori Adı: ")
            description = input("Açıklama: ")

            # category_service = CategoryService()
            # category_service.create_category(name, description)

            CategoryService.create_category({"name": name, "description": description})

        elif choise == "0":
            print("Çıkış yapılıyor...")
        else:
            print("Geçersiz seçim")


if __name__ == "__main__":
    main()
