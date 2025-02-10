
# MongoDB Tools Kurulumu ve Veri İçe/Dışa Aktarma İşlemleri

## **1. MongoDB Tools İndirme**
MongoDB veri import/export işlemlerini gerçekleştirmek için aşağıdaki linkten MongoDB Tools'u indirmeniz gerekmektedir:

🔗 [MongoDB Tools İndirme Linki](https://www.mongodb.com/try/download/database-tools)

## **2. MongoDB Veri İçe Aktarma (Import)**
MongoDB'ye JSON veya CSV formatında veri aktarmak için `mongoimport` komutunu kullanabilirsiniz.

**Not:** Bu işlemleri **CMD (Komut İstemi)** üzerinden ve **MongoDB Server'a bağlı olmadan** yapmanız gerekmektedir.

### **JSON Formatında Veri İçe Aktarma**
```sh
mongoimport --uri "mongodb://localhost:27017" --db Northwind --collection Products --file "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/products.json" --jsonArray

mongoimport --uri "mongodb://localhost:27017" --db Northwind --collection Customers --file "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/customers.json" --jsonArray
```

### **CSV Formatında Veri İçe Aktarma**
```sh
mongoimport --uri "mongodb://localhost:27017" --db Northwind --collection Categories --type csv --file "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/categories.csv" --headerline

mongoimport --uri "mongodb://localhost:27017" --db Northwind --collection Kategoriler --type csv --file "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/categories.csv" --headerline
```

### **Parametre Açıklamaları:**
- `--uri` → MongoDB bağlantı adresi (Cloud veya local olabilir).
- `--db` → Hedef veritabanı.
- `--collection` → Hedef koleksiyon.
- `--file` → Kaynak dosyanın yolu.

## **3. MongoDB Koleksiyon Adı Değiştirme**
Bir koleksiyonun adını değiştirmek için aşağıdaki komutu kullanabilirsiniz:
```js
db.adminCommand({renameCollection: "Northwind.Customers", to: "Northwind.Products"})
```

## **4. MongoDB Alan (Field) Adı Değiştirme**
Mevcut koleksiyon içerisindeki bir alanın adını değiştirmek için:
```js
db.Kategoriler.updateMany({}, {$rename:{ 'CategoryName':'categoryName'}})
```

## **5. MongoDB Veri Dışa Aktarma (Export)**
MongoDB'den JSON veya CSV formatında veri dışa aktarmak için `mongoexport` komutunu kullanabilirsiniz.

### **JSON Formatında Veri Dışa Aktarma**
```sh
mongoexport --uri "mongodb://localhost:27017" --db Northwind --collection Customers --out "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/e-customers.json" --jsonArray
```

**Belirli Alanları Seçerek JSON Formatında Dışa Aktarma**
```sh
mongoexport --uri "mongodb://localhost:27017" --db Northwind --collection Customers --out "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/x-customers.json" --jsonArray --fields CompanyName,ContactName
```

### **CSV Formatında Veri Dışa Aktarma**
```sh
mongoexport --uri "mongodb://localhost:27017" --db Northwind --collection Customers --type csv --out "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/x-customers.csv" --fields CompanyName,ContactName
```

### **Belirli Bir Koşula Göre JSON Formatında Veri Dışa Aktarma**
```sh
mongoexport --uri "mongodb://localhost:27017" --db Northwind --collection Products --out "C:/Users/murat/OneDrive/Desktop/mongodb-egitim/examples/day-4/ex-products.json" --query "{"UnitPrice": { "$gte": 30 }}"  --fields ProductID,ProductName,UnitPrice,UnitsInStock,CategoryID
```

## **6. Regex Kullanımı ile Veri Filtreleme**
Kategori isimlerinde belirli bir kelimeyi içerenleri bulmak için:
```js
{ "CategoryName": {"$regex": "po", $options: "i" }}
```

Bu komut, `CategoryName` alanında `"po"` geçen (büyük/küçük harfe duyarsız) tüm kayıtları döndürür.
