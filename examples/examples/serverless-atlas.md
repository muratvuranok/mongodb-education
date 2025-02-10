# MongoDB Atlas & Serverless (Bulut Tabanlı MongoDB Kullanımı)

## 📌 1. Giriş

MongoDB Atlas, **MongoDB'nin tam yönetilen bir bulut hizmetidir**.  
**Serverless (sunucusuz) mimari**, ihtiyaca göre ölçeklenen ve **altyapı yönetimi gerektirmeyen** bir veri tabanı çözümüdür.

✅ **Bu rehberde şunları öğreneceğiz:**  
- **MongoDB Atlas Üzerinde Cluster Yönetimi**
- **MongoDB Atlas ile AWS Lambda ve Azure Functions Kullanımı**
- **Serverless Querying ve Performans Optimizasyonu**
- **Atlas Search & Vector Search Entegrasyonu**
- **MongoDB Atlas ile Kafka, ElasticSearch ve BI Connector Kullanımı**

---

## 📌 2. MongoDB Atlas Üzerinde Cluster Yönetimi

### **🔹 2.1 Atlas Üzerinde Yeni Bir Cluster Oluşturma**

MongoDB Atlas’ta yeni bir cluster oluşturmak için:
1. **MongoDB Atlas hesabına giriş yap** ([https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)).
2. **"Create a New Cluster"** butonuna tıkla.
3. **Cloud Provider (AWS, Azure, GCP)** seç.
4. **Region (Bölge) belirle** (Daha düşük latency için en yakın olanı seç).
5. **Cluster boyutunu belirle (M0 - Free Tier, M10, M20, vb.)**.

✅ **Önerilen Ayarlar:**  
- **Geliştirme için:** M0 (Ücretsiz Katman)  
- **Üretim için:** M10 veya daha üstü  
- **Büyük Ölçekli Sistemler için:** Multi-Region Cluster  

---

## 📌 3. MongoDB Atlas ile AWS Lambda ve Azure Functions Kullanımı

MongoDB Atlas, **AWS Lambda** ve **Azure Functions** gibi **Serverless çözümlerle** entegre edilebilir.

### **🔹 3.1 AWS Lambda ile MongoDB Atlas Kullanımı**

✅ **Gerekli Bağımlılıkları Yükle**

```sh
npm install mongodb aws-sdk
```

✅ **AWS Lambda içinde MongoDB Atlas Bağlantısı**

```javascript
const { MongoClient } = require("mongodb");

const uri = process.env.MONGO_URI; // Environment variable
let client;

exports.handler = async (event) => {
    if (!client) {
        client = new MongoClient(uri);
        await client.connect();
    }

    const db = client.db("serverlessDB");
    const users = await db.collection("users").find().toArray();

    return {
        statusCode: 200,
        body: JSON.stringify(users),
    };
};
```

📌 **Bu AWS Lambda fonksiyonu, MongoDB Atlas'tan `users` koleksiyonundaki verileri getirir.**

---

### **🔹 3.2 Azure Functions ile MongoDB Atlas Kullanımı**

✅ **Azure Function içindeki MongoDB Bağlantısı**

```javascript
const { MongoClient } = require("mongodb");

module.exports = async function (context, req) {
    const client = new MongoClient(process.env.MONGO_URI);
    await client.connect();

    const db = client.db("serverlessDB");
    const users = await db.collection("users").find().toArray();

    context.res = {
        status: 200,
        body: users,
    };
};
```

📌 **Azure Functions ile aynı kod AWS Lambda'daki gibi çalışır.**

---

## 📌 4. Serverless Querying ve Performans Optimizasyonu

MongoDB Atlas, **Serverless Querying (Sunucusuz Sorgulama)** destekler.

### **🔹 4.1 Serverless Querying için En İyi Uygulamalar**

✅ **Indexing Kullanın:**

```javascript
db.users.createIndex({ email: 1 });
```

✅ **Aggregation Pipelines Kullanarak Performansı Artırın:**

```javascript
db.orders.aggregate([
    { $match: { status: "shipped" } },
    { $group: { _id: "$customerId", totalSpent: { $sum: "$amount" } } },
]);
```

✅ **Idle Connection'ları Kapatın (AWS Lambda / Azure Functions için)**

```javascript
await client.close();
```

---

## 📌 5. Atlas Search & Vector Search Entegrasyonu

MongoDB **Atlas Search**, tam metin arama ve vektör tabanlı aramaları destekler.

### **🔹 5.1 Atlas Search Kullanımı (Full-Text Search)**

✅ **Atlas Search Index Tanımlama**

```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "description": {
        "type": "autocomplete"
      }
    }
  }
}
```

✅ **Atlas Search Query Örneği**

```javascript
db.products.aggregate([
    {
        $search: {
            index: "product_search",
            autocomplete: {
                query: "laptop",
                path: "description",
                fuzzy: { maxEdits: 2 }
            }
        }
    }
]);
```

### **🔹 5.2 Atlas Vector Search Kullanımı (AI Entegrasyonu)**

MongoDB **Vector Search**, AI ve makine öğrenimi modelleriyle **vektör tabanlı benzerlik araması yapar**.

✅ **Vektör Index Tanımlama**

```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "type": "knnVector",
        "dimensions": 1536,
        "similarity": "cosine"
      }
    }
  }
}
```

✅ **Vektör Araması Sorgusu**

```json
{
  "queryVector": [0.12, 0.56, 0.98],
  "path": "embedding",
  "numCandidates": 100,
  "limit": 5
}
```

📌 **Bu yapı, AI modellerinden gelen embedding’leri MongoDB üzerinde aramaya yarar.**

---

## 📌 6. MongoDB Atlas ile Kafka, ElasticSearch ve BI Connector Kullanımı

MongoDB Atlas, **Kafka, ElasticSearch ve BI araçları** ile entegre olabilir.

### **🔹 6.1 MongoDB Kafka Connector ile Entegrasyon**

✅ **Kafka Connector Yükleme**

```sh
confluent-hub install mongodb/kafka-connect-mongodb:1.7.0
```

✅ **Kafka Connector Konfigürasyonu (`mongodb-source.json`)**

```json
{
  "name": "mongodb-connector",
  "config": {
    "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
    "connection.uri": "mongodb://localhost:27017",
    "database": "ecommerce",
    "collection": "orders",
    "topic.prefix": "mongo-changes",
    "poll.max.batch.size": "1000"
  }
}
```

✅ **Kafka Konnektörü Çalıştırma**

```sh
curl -X POST -H "Content-Type: application/json" --data @mongodb-source.json http://localhost:8083/connectors
```

---

### **🔹 6.2 MongoDB Atlas ile ElasticSearch Entegrasyonu**

MongoDB’den ElasticSearch’e veri göndermek için **MongoDB Connector for ElasticSearch** kullanılır.

✅ **Connector Kurulumu:**

```sh
confluent-hub install mongodb/kafka-connect-elasticsearch:1.5.0
```

✅ **Atlas ile ElasticSearch Bağlantısını Kurma**

```json
{
  "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
  "connection.uri": "mongodb://atlas.mongodb.net",
  "database": "logs",
  "collection": "events",
  "topic.prefix": "es-events"
}
```

📌 **Bu konfigürasyon MongoDB Atlas ile ElasticSearch arasındaki veri akışını sağlar.**

---

## 📌 7. Sonuç

✅ **MongoDB Atlas ile serverless kullanımını öğrendik.**  
✅ **AWS Lambda ve Azure Functions entegrasyonlarını gördük.**  
✅ **Atlas Search ve Vector Search ile AI destekli sorgular yaptık.**  
✅ **Kafka, ElasticSearch ve BI Connector entegrasyonlarını öğrendik.**  

🚀 **MongoDB Atlas’ı serverless ve büyük ölçekli sistemlerde verimli kullanabilirsin!**  
