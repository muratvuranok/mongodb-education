# MongoDB Performance Tuning (Performans Optimizasyonu)

## 📌 1. Giriş
MongoDB’de yüksek performans elde etmek için **index kullanımı, sorgu analizi, bellek yönetimi, bağlantı havuzu ve paralel sorgu çalıştırma tekniklerini** bilmek önemlidir.

Bu rehberde, **MongoDB’nin performansını artırmaya yönelik en iyi uygulamalar** ele alınacaktır.

---

## 📌 2. Index Kullanımı ve Optimizasyonu

**İndeksler**, MongoDB'deki sorguların hızlanmasını sağlayan en önemli araçlardan biridir. Eğer indeksler doğru kullanılmazsa, sorgular **full collection scan (tüm koleksiyonu tarama)** yaparak performansı düşürebilir.

### **🔹 2.1 Single Field Index (Tek Alanlı İndeks)**
Bir alana indeks ekleyerek sorguların daha hızlı çalışmasını sağlayabiliriz.

✅ **Örnek:**

```javascript
db.users.createIndex({ email: 1 }); // email alanına artan sıralı indeks
```

Bu indeks, aşağıdaki sorguları hızlandıracaktır:

```javascript
db.users.find({ email: "murat@example.com" });
```

---

### **🔹 2.2 Compound Index (Bileşik İndeks)**
Birden fazla alan için indeks oluşturabiliriz.

✅ **Örnek:**

```javascript
db.orders.createIndex({ customerId: 1, orderDate: -1 });
```

Bu indeks, aşağıdaki sorguları hızlandırır:

```javascript
db.orders.find({ customerId: 123 }).sort({ orderDate: -1 });
```

**Dikkat:** **İndeksin sırası önemlidir**. `(customerId, orderDate)` indeksini oluşturduğumuzda, **(orderDate, customerId)** sıralamasındaki bir sorguda indeks kullanılamaz.

---

## 📌 3. Özel İndeks Türleri

### **🔹 3.1 TTL Index (Zaman Aşımı İndeksi)**
Belirli bir süre sonra otomatik olarak silinmesi gereken belgeler için kullanılır.

✅ **Örnek:** **Oluşturulduktan 7 gün sonra belgeleri otomatik silen bir indeks**:

```javascript
db.logs.createIndex({ createdAt: 1 }, { expireAfterSeconds: 604800 });
```

---

### **🔹 3.2 Sparse Index (Seyrek İndeks)**
Belirtilen alanı olmayan belgeleri indekslemez. Böylece, gereksiz indeks kaydı önlenir.

✅ **Örnek:**

```javascript
db.users.createIndex({ phoneNumber: 1 }, { sparse: true });
```

Eğer **phoneNumber alanı olmayan belgeler varsa**, **Sparse Index** onları indekslemez ve gereksiz bellek tüketimini azaltır.

---

### **🔹 3.3 Hashed Index (Hashlenmiş İndeks)**
Eşitlik karşılaştırmaları için uygundur, ancak sıralı aramalar için kullanılamaz.

✅ **Örnek:**

```javascript
db.accounts.createIndex({ accountNumber: "hashed" });
```

Bu indeks, yalnızca **eşitlik aramalarını** hızlandırır:

```javascript
db.accounts.find({ accountNumber: "TR123456" });
```

Ancak şu sorgular **hashed index ile hızlanmaz**:

```javascript
db.accounts.find({ accountNumber: { $gt: "TR1000" } }); // Çalışmaz!
```

---

## 📌 4. Profiling & Slow Query Analysis

MongoDB'de **yavaş sorguları (slow queries)** tespit etmek için **profiling mekanizmasını** kullanabiliriz.

### **🔹 4.1 Profiling Seviyelerini Ayarlama**
MongoDB’de `profilingLevel` şu değerleri alabilir:

| Seviye | Açıklama |
|--------|---------|
| `0` | Profiling kapalı |
| `1` | Yavaş sorgular kaydedilir |
| `2` | Tüm sorgular kaydedilir |

✅ **Örnek:** **Yavaş sorguları (100ms üzeri) loglamak için**:

```javascript
db.setProfilingLevel(1, 100);
```

✅ **Örnek:** **Son 5 yavaş sorguyu görmek için**:

```javascript
db.system.profile.find().sort({ millis: -1 }).limit(5);
```

Bu sorgu, en uzun sürede tamamlanan sorguları listeler.

---

## 📌 5. Query Plan Analizi (`explain("executionStats")`)

MongoDB, **hangi indekslerin kullanıldığını ve sorguların nasıl çalıştığını analiz etmek için** `explain("executionStats")` metodunu sağlar.

✅ **Örnek:**

```javascript
db.orders.find({ customerId: 123 }).explain("executionStats");
```

Bu komut, MongoDB’nin **hangi indeksleri kullandığını, kaç belgeyi taradığını ve sorgunun kaç milisaniyede çalıştığını gösterir**.

📌 **Eğer `executionStats` içinde `COLLSCAN` görüyorsan, indeks kullanmıyorsun demektir ve performans sorunları yaşayabilirsin!**

---

## 📌 6. Memory Management ve Cache Kullanımı

MongoDB, **bellek yönetimini (memory management) ve disk I/O işlemlerini optimize etmek için WiredTiger Cache kullanır**.

### **🔹 6.1 WiredTiger Cache Yönetimi**
WiredTiger cache varsayılan olarak **RAM’in %50’sini** kullanır. Eğer bu değeri değiştirmek istiyorsan:

✅ **Örnek:**

MongoDB yapılandırma dosyasında (`mongod.conf`):

```yaml
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2
```

Bu ayar, **maksimum 2GB bellek kullanımını zorunlu kılar**.

---

## 📌 7. Connection Pooling ve Parallel Query Execution

MongoDB, **çok sayıda istemciyi aynı anda desteklemek için bağlantı havuzu (connection pooling) kullanır**.

### **🔹 7.1 Connection Pool Ayarları**

Eğer **Node.js MongoDB Driver** kullanıyorsan, bağlantı havuzunu şu şekilde optimize edebilirsin:

```javascript
const { MongoClient } = require('mongodb');

const client = new MongoClient("mongodb://localhost:27017", {
  poolSize: 50, // Maksimum 50 bağlantı
  useNewUrlParser: true,
  useUnifiedTopology: true
});
```

### **🔹 7.2 Paralel Query Execution (Aynı Anda Çoklu Sorgu Çalıştırma)**

MongoDB, **aynı anda birden fazla sorgunun çalışmasına izin verir**. Bu yüzden **büyük verileri paralel işle**.

✅ **Örnek:**

```javascript
async function runQueriesInParallel() {
    const [result1, result2] = await Promise.all([
        db.collection("orders").find({ status: "shipped" }).toArray(),
        db.collection("customers").find({ city: "Istanbul" }).toArray()
    ]);
}
```

Bu kod, iki sorguyu **paralel olarak** çalıştırarak **bekleme süresini azaltır**.

---

## 📌 8. Sonuç
✅ **İndeks kullanımı ve optimizasyonlarını öğrendik.**  
✅ **TTL, Sparse ve Hashed indekslerin nasıl kullanıldığını gördük.**  
✅ **Profiling ile yavaş sorguları analiz ettik.**  
✅ **Query Plan Analizi ile MongoDB’nin nasıl çalıştığını öğrendik.**  
✅ **Bellek yönetimi ve bağlantı havuzlarını optimize ettik.**  
✅ **Paralel sorgular ile performansı artırdık.**  

🚀 **MongoDB performans optimizasyonu konusunda artık daha bilinçli kararlar alabilirsin!**  
