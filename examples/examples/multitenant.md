# Multi-Tenancy with MongoDB (Çoklu Kiracı Mimarisi)

## 📌 1. Giriş
**Multi-Tenancy (Çoklu Kiracı Mimarisi)**, aynı sistemin birden fazla **müşteri (tenant)** için izole veya paylaşımlı olarak çalışmasını sağlar.  
MongoDB, **multi-tenant mimarisi** için **esnek veri modelleme seçenekleri** sunar.

**Neden Multi-Tenancy Kullanmalıyız?**  
✅ **Veri izolasyonu sağlamak** (her müşterinin verisini ayrı tutmak)  
✅ **Ölçeklenebilirliği artırmak** (büyüyen müşteri sayısını yönetebilmek)  
✅ **Performans optimizasyonu yapmak** (veritabanı, koleksiyon veya belge bazında izolasyon)  
✅ **Güvenlik politikalarını uygulamak** (tenant bazlı erişim kontrolü)  

---

## 📌 2. MongoDB'de Multi-Tenant Mimari Nasıl Uygulanır?

MongoDB’de **multi-tenancy uygulamak için 3 farklı yöntem** vardır:

1. **Ayrı Database Kullanımı** (Database Per Tenant)
2. **Ayrı Collection Kullanımı** (Collection Per Tenant)
3. **Ayrı Document Kullanımı** (Single Collection, Document Per Tenant)

---

## 📌 3. Multi-Tenancy Stratejileri

### **🔹 3.1 Ayrı Database Kullanımı (Database Per Tenant)**
**Her müşteri (tenant) için ayrı bir veritabanı oluşturulur.**

✅ **Avantajlar:**  
- **Veri izolasyonu en üst seviyededir.**
- **Yetkilendirme (RBAC) daha kolay yönetilir.**
- **Farklı ölçeklenme politikaları uygulanabilir.**

❌ **Dezavantajlar:**  
- **Çok fazla müşteri varsa veritabanı yönetimi zorlaşır.**
- **MongoDB'nin maksimum `100.000` database sınırına yaklaşabilir.**

📌 **Örnek:**

```javascript
const db1 = client.db("tenant1_db");
const db2 = client.db("tenant2_db");

db1.collection("users").insertOne({ name: "Ali" });
db2.collection("users").insertOne({ name: "Ayşe" });
```

---

### **🔹 3.2 Ayrı Collection Kullanımı (Collection Per Tenant)**
**Her müşteri için ayrı bir koleksiyon oluşturulur.**

✅ **Avantajlar:**  
- **Orta seviyede veri izolasyonu sağlar.**
- **Index yönetimi daha verimlidir.**
- **Çok fazla müşteri varsa yönetimi daha kolaydır.**

❌ **Dezavantajlar:**  
- **Çok fazla koleksiyon olduğunda sorguların performansı düşebilir.**
- **Indexing yönetimi karmaşık hale gelebilir.**

📌 **Örnek:**

```javascript
const db = client.db("multi_tenant_db");

db.collection("tenant1_users").insertOne({ name: "Ali" });
db.collection("tenant2_users").insertOne({ name: "Ayşe" });
```

---

### **🔹 3.3 Aynı Collection İçinde Tenant ID Kullanımı (Single Collection, Document Per Tenant)**
**Tüm müşteriler aynı koleksiyonda tutulur, ancak `tenantId` ile ayrıştırılır.**

✅ **Avantajlar:**  
- **Şema yönetimi kolaydır.**
- **Tüm müşterilere yönelik analizleri ve sorguları çalıştırmak daha hızlıdır.**
- **Indexleme stratejileri ile optimize edilebilir.**

❌ **Dezavantajlar:**  
- **Büyük ölçekli sistemlerde tek koleksiyon şişebilir.**
- **Tenant bazlı veri izolasyonu daha karmaşık hale gelebilir.**

📌 **Örnek:**

```javascript
db.collection("users").insertMany([
    { tenantId: "tenant1", name: "Ali" },
    { tenantId: "tenant2", name: "Ayşe" }
]);

// Belirli bir tenant için sorgu yaparken
db.collection("users").find({ tenantId: "tenant1" });
```

---

## 📌 4. Indexing ve Query Performance Yönetimi

MongoDB'de **multi-tenant sistemlerde performans yönetimi** için **doğru indeksleme stratejileri** belirlenmelidir.

### **🔹 4.1 Tenant ID'ye Göre Index Kullanımı**
Eğer **aynı koleksiyonu tüm müşteriler kullanıyorsa**, **tenantId** üzerine indeks eklemek önemlidir.

✅ **Örnek:**

```javascript
db.users.createIndex({ tenantId: 1 });
```

Bu indeks sayesinde **tenant bazlı sorgular** daha hızlı çalışır.

---

### **🔹 4.2 Compound Index Kullanımı**
Eğer **tenant bazlı sık sorgular** yapılıyorsa, **bileşik indeksler (compound index)** kullanılabilir.

✅ **Örnek:**

```javascript
db.orders.createIndex({ tenantId: 1, orderDate: -1 });
```

Bu indeks, **belirli bir tenant için siparişleri tarih sırasına göre hızlı getirir.**

---

## 📌 5. MongoDB Realm & Stitch ile Çoklu Tenant Yönetimi

**MongoDB Realm & Stitch**, **multi-tenant mimarilerde güvenlik ve erişim yönetimini** sağlar.

### **🔹 5.1 Stitch Kullanarak Yetkilendirme**
MongoDB **Stitch**, tenant bazlı erişimi kolaylaştırır.

✅ **Örnek: Role-Based Access Control (RBAC) Kullanımı**

```json
{
  "roles": [
    {
      "role": "readWrite",
      "database": "tenant1_db",
      "collection": "orders"
    }
  ]
}
```

Bu yapılandırma, sadece **tenant1 için `orders` koleksiyonunda okuma/yazma izni** verir.

---

### **🔹 5.2 MongoDB Realm Kullanarak JWT ile Tenant Yönetimi**
MongoDB Realm, JWT token içinde **tenantId** bilgisini kullanarak erişimi kontrol edebilir.

✅ **Örnek: Kullanıcıya Özel Query Filtreleme**

```json
{
  "rules": {
    "orders": {
      "read": {
        "tenantId": "%%user.custom_data.tenantId"
      }
    }
  }
}
```

Bu kurallar sayesinde, **kullanıcı sadece kendi tenant’ına ait verilere erişebilir.**

---

## 📌 6. Sonuç

✅ **MongoDB'de multi-tenancy mimarisi için 3 farklı yöntemi öğrendik:**  
1️⃣ **Her tenant için ayrı veritabanı (Database Per Tenant)**  
2️⃣ **Her tenant için ayrı koleksiyon (Collection Per Tenant)**  
3️⃣ **Tüm tenant'ları tek koleksiyonda yönetme (Document Per Tenant)**  

✅ **Indexleme ve performans yönetimini öğrendik.**  
✅ **MongoDB Realm & Stitch ile tenant bazlı yetkilendirmeyi inceledik.**  

🚀 **Multi-tenancy yapısına ihtiyacın varsa, hangi yöntemin uygun olduğunu iş modeline göre seçebilirsin!**  
