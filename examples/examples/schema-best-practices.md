# MongoDB Schema Design & Best Practices (Şema Tasarımı ve En İyi Uygulamalar)

## 📌 1. Giriş
MongoDB, **esnek ve ölçeklenebilir bir NoSQL veritabanıdır**. Ancak, doğru şema tasarlamak **performans, veri bütünlüğü ve ölçeklenebilirlik açısından kritik öneme sahiptir**.

Bu rehberde şema tasarımı konusunda **en iyi uygulamaları ve karşılaştırmaları** öğreneceğiz.

---

## 📌 2. Embed vs Reference (İç İçe mi Yoksa Referans mı?)
MongoDB'de veriyi iki şekilde saklayabilirsin:
- **Embedded Documents (İç İçe Dokümanlar)**
- **Referenced Documents (Referanslı Dokümanlar - Normalization)**

| Kriter | Embedded (İç İçe) | Referenced (Referanslı) |
|--------|----------------|----------------|
| **Veri Okuma Hızı** | Daha hızlı, tek sorgu yeterli | Daha yavaş, ek sorgular gerekebilir |
| **Veri Güncelleme** | Büyük dokümanlarda güncelleme maliyeti artar | Güncellemeler daha verimli olabilir |
| **Veri Tekrarı** | Aynı veri birden fazla kayıtta olabilir (denormalizasyon) | Daha az tekrar, ilişkisel yapı |
| **Ölçeklenebilirlik** | Küçük veri setleri için uygun | Büyük ölçekli sistemler için daha iyi |
| **Sharding Uygunluğu** | Büyük dokümanlar shard üzerinde problem yaratabilir | Daha iyi ölçeklenebilirlik sağlar |

**🔹 Hangi Durumda Ne Kullanmalıyız?**
- **Sık kullanılan ve çok ilişkili veriler** için **Embedded** kullan.
- **Büyük ve sık güncellenen veriler** için **Referenced** kullan.

📌 **Örnek: Kullanıcıların Siparişlerini Saklama**  
**Senaryo:** Bir kullanıcının siparişlerini saklıyoruz.

✅ **Embedded Kullanımı:** Kullanıcının siparişleri çok küçükse, iç içe tutabiliriz.

```json
{
  "_id": 1,
  "name": "Murat Vuranok",
  "orders": [
    { "order_id": 101, "total": 50.0, "date": "2024-02-05" },
    { "order_id": 102, "total": 30.0, "date": "2024-02-06" }
  ]
}
```

✅ **Referenced Kullanımı:** Siparişler çok büyükse ve ilişkili başka verilerle kullanılacaksa, referans yapabiliriz.

```json
{
  "_id": 1,
  "name": "Murat Vuranok",
  "orders": [101, 102]
}
```

```json
{
  "_id": 101,
  "customer_id": 1,
  "total": 50.0,
  "date": "2024-02-05"
}
```

---

## 📌 3. One-to-One, One-to-Many, Many-to-Many İlişkileri
### 🔹 **One-to-One (Bire-Bir İlişki)**
**Örnek:** Kullanıcı ve profil bilgisi

```json
{
  "_id": 1,
  "name": "Murat",
  "profile": {
    "age": 30,
    "email": "murat@example.com"
  }
}
```

Alternatif olarak, **referanslı** olarak tutabiliriz:

```json
{
  "_id": 1,
  "name": "Murat",
  "profile_id": 101
}
```

```json
{
  "_id": 101,
  "age": 30,
  "email": "murat@example.com"
}
```

---

### 🔹 **One-to-Many (Bire-Çok İlişki)**
**Örnek:** Bir ürünün yorumları

✅ **Embedded Kullanımı:**

```json
{
  "_id": 1,
  "name": "Laptop",
  "reviews": [
    { "user": "Ali", "rating": 5, "comment": "Harika!" },
    { "user": "Ayşe", "rating": 4, "comment": "Fena değil" }
  ]
}
```

✅ **Referenced Kullanımı:**

```json
{
  "_id": 1,
  "name": "Laptop"
}
```

```json
{
  "_id": 101,
  "product_id": 1,
  "user": "Ali",
  "rating": 5,
  "comment": "Harika!"
}
```

---

### 🔹 **Many-to-Many (Çoktan-Çoka İlişki)**
**Örnek:** Kullanıcılar ve roller

```json
{
  "_id": 1,
  "name": "Murat",
  "roles": ["admin", "editor"]
}
```

Veya ayrı bir koleksiyon kullanabiliriz:

```json
{
  "_id": 101,
  "user_id": 1,
  "role": "admin"
}
```

---

## 📌 4. Denormalization ve Performans Yönetimi
**Denormalization (Veri Tekrarı Kullanma)** bazı durumlarda sorgu performansını artırabilir.

✅ **Örnek:** Kullanıcının siparişleriyle ilgili bilgileri **tekrarlamak**:

```json
{
  "_id": 101,
  "customer": {
    "id": 1,
    "name": "Murat"
  },
  "total": 50.0
}
```

Denormalization, **okuma hızını artırırken** veri boyutunu artırabilir.

---

## 📌 5. Sharding & Partitioning için Uygun Şema Tasarımları
**Sharding yaparken dikkat edilmesi gerekenler:**

- **Shard Key Seçimi**: Dengeli bir dağılım sağlayan alanlar kullanılmalı.
- **Büyük embedded dökümanlar parçalanabilir**.
- **Uygun Indexing Kullanımı**.

✅ **Örnek:** Shard edilen bir koleksiyon

```javascript
sh.enableSharding("ecommerce");
sh.shardCollection("ecommerce.orders", { "customerId": "hashed" });
```

---

## 📌 6. Polyglot Persistence (Farklı Veri Modelleri ile MongoDB Kullanımı)
MongoDB'yi başka veri tabanlarıyla birlikte kullanabilirsin:

✅ **Örnek: PostgreSQL + MongoDB**  
- **PostgreSQL** → Siparişleri tutmak için  
- **MongoDB** → Kullanıcı aktivitelerini saklamak için

Bu yaklaşım, **doğru veri modelini** doğru veri tabanında tutmayı sağlar.

---

## 📌 7. Sonuç
✅ **Embedded ve Referenced veri modellerini öğrendik.**  
✅ **One-to-One, One-to-Many, Many-to-Many ilişkileri öğrendik.**  
✅ **Denormalization ve performans optimizasyonları yaptık.**  
✅ **Sharding ve Polyglot Persistence hakkında bilgi edindik.**  

🚀 **MongoDB'de şema tasarımını doğru yapmak, hem ölçeklenebilirlik hem de performans açısından kritik öneme sahiptir.**

