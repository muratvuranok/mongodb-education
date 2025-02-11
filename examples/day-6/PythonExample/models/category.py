from bson.objectid import ObjectId


class Category:
    """
    Category modeli, kategori nesnesini temsil eder.
    """

    def __init__(self, name: str, description: str, _id: str = None):
        self._id = (
            ObjectId(_id) if _id else None
        )  # _id is not null ? ObjectId(_id) : None
        self.Name = name.title()  # İlk harfi büyük yap, gereksiz boşlukları kaldır
        self.Description = description.title() 
        
    def __str__(self):
        return f"{self.Name} {self.Description}"

    def to_dict(self):
        """
        Kategori nesnesini bir sözlük veri yapısına dönüştürür.

        Bu dönüşüm, JSON formatına kolayca çevrilebilmesini ve MongoDB gibi NoSQL
        veritabanlarında saklanmasını sağlar.

        Returns:
            dict: Kategori nesnesinin sözlük formatında temsilini döndürür.
                - "Name" (str): Kategorinin adı.
                - "Description" (str): Kategorinin açıklaması.

        Raises:
            AttributeError: Eğer nesnede beklenen bir özellik bulunamazsa hata fırlatır.

        Example:
            Bir kategori nesnesini sözlük formatına çevirme:

            >>> c = Category("Beverages", "test")
            >>> c.to_dict()
            {'Name': 'Beverages', 'Description': 'test'}

        Usage:
            - JSON formatına çevirmek için:
                >>> import json
                >>> json.dumps(c.to_dict())

            - MongoDB'ye eklerken kullanılabilir:
                >>> db.categories.insert_one(c.to_dict())

        Notes:
            - Bu metod yalnızca `Name` ve `Description` alanlarını döndürür.
            Eğer ek alanlar varsa, genişletilmesi gerekebilir.
            - MongoDB `_id` alanını otomatik oluşturur, bu yüzden burada belirtilmemiştir.

        See Also:
            - `json.dumps()`: JSON formatına çevirme fonksiyonu.
            - `pymongo.collection.Collection.insert_one()`: MongoDB’ye belge ekleme fonksiyonu.
        """

        data = {"Name": self.Name, "Description": self.Description}
        if self._id:
            data["_id"] = ObjectId(
                self._id
            )  # _id değerini ObjectId değeri olarak ekler.

        return data


# record Category(string Name, string Description);
