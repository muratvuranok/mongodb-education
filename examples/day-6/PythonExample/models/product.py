from bson.objectid import ObjectId


class Product:
    """
    MongoDB için Ürün (Product) modeli.
    """

    def __init__(
        self,
        name: str,
        price: float,
        units_in_stock: int,
        category_id: str,
        _id: str = None,
    ):
        """
        Ürün modelinin constructor'ı.

        Args:
            name (str): Ürün adı.
            price (float): Ürün fiyatı.
            units_in_stock (int): Stoktaki ürün adedi.
            category_id (str): Bağlı olduğu kategori ID'si.
            _id (str, optional): MongoDB ObjectId. Varsayılan olarak None.
        """
        self._id = (
            ObjectId(_id) if _id else None
        )  # Eğer _id varsa ObjectId olarak çevir
        self.name = (
            name.strip().title()
        )  # İlk harfi büyük yap, gereksiz boşlukları kaldır
        self.price = round(float(price), 2)  # Fiyatı yuvarla (örneğin 10.5999 → 10.6)
        self.units_in_stock = int(units_in_stock)  # Stok adedini integer yap
        self.category_id = (
            ObjectId(category_id) if category_id else None
        )  # Kategori ID'yi ObjectId olarak kaydet

    def __str__(self):
        """
        Nesneyi string olarak döndürür.
        """
        return f"Product(Name={self.name}, Price={self.price}, Stock={self.units_in_stock}, CategoryId={self.category_id})"

    def to_dict(self):
        """
        Ürünü MongoDB'ye eklenebilir bir sözlüğe dönüştürür.

        Returns:
            dict: Ürün verisini sözlük formatında döndürür.
        """
        data = {
            "name": self.name,
            "price": self.price,
            "units_in_stock": self.units_in_stock,
            "category_id": self.category_id,
        }
        if self._id:
            data["_id"] = self._id  # MongoDB _id alanını ekle
        return data
