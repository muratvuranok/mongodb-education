# MongoDB Change Streams (Gerçek Zamanlı Veri İzleme)

## 📌 1. Change Streams Nedir?
MongoDB **Change Streams**, veritabanında yapılan değişiklikleri **gerçek zamanlı olarak izlememizi** sağlar.  
Bu özellik sayesinde, **insert, update, delete** gibi olaylar tetiklendiğinde **gerçek zamanlı aksiyonlar alabiliriz**.

Change Streams, özellikle **event-driven (olay güdümlü) mimarilerde** ve **veri senkronizasyonu gerektiren uygulamalarda** kullanılır.

---

## 📌 2. MongoDB'de Gerçek Zamanlı Değişiklikleri Nasıl İzleriz?

MongoDB’de bir koleksiyonda yapılan değişiklikleri izlemek için **watch()** metodunu kullanabiliriz.

### **🔹 2.1 Koleksiyon Bazlı Change Stream**

Aşağıdaki örnek, `orders` koleksiyonundaki değişiklikleri izler:

```javascript
const { MongoClient } = require("mongodb");

async function watchChanges() {
    const client = new MongoClient("mongodb://localhost:27017");
    await client.connect();
    
    const db = client.db("ecommerce");
    const collection = db.collection("orders");

    const changeStream = collection.watch();

    changeStream.on("change", (change) => {
        console.log("Değişiklik Algılandı:", change);
    });
}

watchChanges();
```

📌 **Bu kod ile:**  
- `orders` koleksiyonundaki değişiklikler anında yakalanır.  
- Yeni sipariş eklendiğinde veya güncellendiğinde olay tetiklenir.

**Çıktı Örneği:**

```json
{
  "operationType": "insert",
  "fullDocument": { "_id": 1, "customerId": 123, "total": 50.0 },
  "ns": { "db": "ecommerce", "coll": "orders" }
}
```

Bu olay, **yeni bir sipariş eklendiğinde** oluşur.

---

### **🔹 2.2 Tüm Veritabanını İzleme**
Bütün veritabanındaki değişiklikleri dinlemek için:

```javascript
const db = client.db("ecommerce");
const changeStream = db.watch();

changeStream.on("change", (change) => {
    console.log("Veritabanı Seviyesinde Değişiklik:", change);
});
```

📌 **Bu kod, aynı anda tüm koleksiyonlardaki değişiklikleri izler.**

---

### **🔹 2.3 Sharded Cluster'da Change Stream Kullanımı**

Sharded Cluster'da **global seviyede değişiklikleri izlemek** için `mongos` üzerinden bağlanmalısın:

```javascript
const mongosClient = new MongoClient("mongodb://mongos-router:27017");
const globalStream = mongosClient.watch();

globalStream.on("change", (change) => {
    console.log("Global Değişiklik:", change);
});
```

Bu yöntem, **büyük ölçekli dağıtılmış sistemlerde değişiklikleri merkezi olarak izlemek** için kullanılır.

---

## 📌 3. Kafka ve MongoDB Change Streams Entegrasyonu

MongoDB'den **Kafka'ya veri göndermek** için **MongoDB Kafka Connector** kullanılabilir.

### **🔹 3.1 MongoDB Kafka Connector Kurulumu**

Öncelikle **Kafka Connector’ü indirip kurulumu yapmalısın**.

```sh
confluent-hub install mongodb/kafka-connect-mongodb:1.7.0
```

### **🔹 3.2 Kafka'ya MongoDB Değişikliklerini Gönderme**

Kafka Connector için **konfigürasyon dosyası (`mongodb-source.json`)**:

```json
{
  "name": "mongodb-connector",
  "config": {
    "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
    "connection.uri": "mongodb://localhost:27017",
    "database": "ecommerce",
    "collection": "orders",
    "pipeline": "[{ $match: { operationType: { $in: ['insert', 'update'] } } }]",
    "topic.prefix": "mongo-changes",
    "poll.max.batch.size": "1000",
    "poll.await.time.ms": "5000"
  }
}
```

Bu yapılandırma:
- **`ecommerce.orders` koleksiyonundaki değişiklikleri `mongo-changes` Kafka konusuna aktarır.**

Konfigürasyonu Kafka'ya yüklemek için:

```sh
curl -X POST -H "Content-Type: application/json" --data @mongodb-source.json http://localhost:8083/connectors
```

Kafka Consumer ile MongoDB değişikliklerini okuyabilirsin:

```sh
kafka-console-consumer --bootstrap-server localhost:9092 --topic mongo-changes --from-beginning
```

---

## 📌 4. Trigger Bazlı Event-Driven Mimari

Change Streams kullanarak **event-driven mimari oluşturabiliriz**. Örneğin, yeni bir sipariş geldiğinde **otomatik olarak fatura oluşturma**:

### **🔹 4.1 Yeni Sipariş Geldiğinde Otomatik Fatura Oluşturma**
```javascript
const changeStream = db.collection("orders").watch();

changeStream.on("change", async (change) => {
    if (change.operationType === "insert") {
        console.log("Yeni Sipariş:", change.fullDocument);
        
        // Fatura oluştur
        await db.collection("invoices").insertOne({
            orderId: change.fullDocument._id,
            amount: change.fullDocument.total,
            createdAt: new Date()
        });

        console.log("Fatura Oluşturuldu!");
    }
});
```

📌 **Bu kod:**
- **Yeni siparişleri izler.**
- **Yeni sipariş geldiğinde, otomatik olarak fatura oluşturur.**

---

## 📌 5. Sonuç
✅ **Change Streams ile MongoDB’de gerçek zamanlı veri izlemeyi öğrendik.**  
✅ **Kafka ile Change Streams entegrasyonunu yaptık.**  
✅ **Trigger bazlı event-driven mimari kurduk.**  

🚀 **MongoDB Change Streams sayesinde, event-driven sistemler oluşturabilir ve değişiklikleri anında işleyebilirsin!**  
