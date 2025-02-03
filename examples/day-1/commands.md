# MongoDB Shell Kullanımı

## MongoDB'ye Bağlanma
```sh
mongosh
```

## Var Olan Veri Tabanlarını Listeleme
```sh
show dbs
```

## Veri Tabanı Seçme
```sh
use <databasename>
```

## Collections (Tablolar) Listeleme
```sh
show collections
```

---

## Kayıt Ekleme İşlemleri

### Tekil Kayıt Ekleme
```sh
use northwind

db.categories.insertOne({ "name": "Beverages", "description": "Soft, Tea" })
```

### Kayıtları Listeleme
```sh
db.categories.find()
```

### Toplu Kayıt Ekleme (Bulk Insert)
```sh
db.categories.insertMany([
    { "name": "c1", "description": "d1" },
    { "name": "c2", "description": "d2" },
    { "name": "c3", "description": "d3" },
    { "name": "c4", "description": "d4" }
])
```

---

## Güncelleme İşlemleri

### Tekil Kayıt Güncelleme
```sh
db.categories.updateOne( 
     { _id: ObjectId('67a07d1df969ecfcc00d8192') },
     { $set: { name: "air_food" }}
)
```

### Toplu Güncelleme Belirli ID'ler İçin
```sh
db.categories.updateMany(
     { 
        _id: { 
            $in: [
                ObjectId('67a07b13fb3caf62ad0d8190'), 
                ObjectId('67a07beefb3caf62ad0d8191'), 
                ObjectId('67a07d1df969ecfcc00d8190')
            ] 
        } 
    },
    { 
        $set: { 
            name: "yoğun istek üzerine, yeniden güncelledik", 
            why:"talep edildi",
            age: 10 
        } 
    }
)
```

### Tüm Kayıtlara Alan Ekleyerek Güncelleme
```sh
db.categories.updateMany(
    {},
    { $set: { createdDate: new Date() } }
)
```

### Belirli Bir Şarta Göre Güncelleme
```sh
db.categories.updateMany(
    { age: { $gt: 30 } },   // Yaşı 30'dan büyük olanları güncelle
    { $set: { status: "young-new query" } }
)
```

---

## Koleksiyon (Collection) Oluşturma ve Şema Tanımlama

### `users` Koleksiyonunu Şema ile Oluşturma
```sh
db.createCollection(
    "users", 
    {
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["name", "age", "email"],
                properties: {
                    name: {
                        bsonType: "string",
                        description: "İsim alanı zorunludur ve bir string olmalıdır."
                    },
                    age: {
                        bsonType: "int",
                        minimum: 18,
                        description: "Yaş en az 18 olmalıdır."
                    },
                    email: {
                        bsonType: "string",
                        pattern: "^\S+@\S+\.\S+$",
                        description: "Email alanı zorunludur ve geçerli bir formatta olmalıdır."
                    }
                }
            }
        }
    }
)
```

### E-posta Alanına Unique Index Ekleyerek Benzersizlik Sağlama
```sh
db.users.createIndex({ email:1 }, { unique: true })
```

### Yeni Kullanıcı Ekleme
```sh
db.users.insertOne({ 
    "name": "murat vuranok",
    "age": 19,
    "email": "isim@soyisim.com"
})
```

### Yeni Bir Zorunlu Alan (phoneNumber) Ekleme
```sh
db.runCommand({ 
    collMod:"users",
    validator:{
        $jsonSchema:{
            required:["phoneNumber"],
            properties:{
                phoneNumber:{
                    bsonType: "string",
                    pattern:"^[0-9]{10,15}$",
                    description: "Telefon numarası 10 ile 15 hane aralığında olmalıdır, sadece sayısal değer girebilirsiniz ve zorunlu alandır :)"
                }
            }
        }
    }
})
```

### Yeni Kullanıcı Ekleyerek Zorunlu Alanı Kullanma
```sh
db.users.insertOne({ 
    "name": "murat vuranok",
    "age": 19,
    "email": "isim@soyisim.com",
    "phoneNumber": "01234567894"
})
```

---

## Veri Sorgulama İşlemleri

### Belirli Bir Şarta Göre Sorgulama
```sh
db.categories.find({ age: { $gte: 30 } })
```

### Belirli Alanları Döndürerek Sorgulama
```sh
db.categories.find(
    { age: { $gte: 30 } },
    { name: 1, _id: 0 }
)
```

### Birden Fazla Alan Döndürerek Sorgulama
```sh
db.categories.find(
    { age: { $gte: 30 } },
    { name: 1, _id: 0, description: 1 }
)
```

---

## Not: Transaction Eklenecek!

MongoDB'de transaction (işlem) yönetimi ilerleyen bölümlerde detaylandırılacaktır.
