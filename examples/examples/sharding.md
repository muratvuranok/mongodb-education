# MongoDB Sharding - Docker Compose ile Kurulum ve Örnek Senaryo

## 📌 1. MongoDB Sharding Nedir?
MongoDB **sharding**, büyük veri kümelerini birden fazla sunucuya dağıtarak ölçeklenebilirliği ve performansı artıran bir yatay bölme (**horizontal partitioning**) yöntemidir.

### **Sharding Bileşenleri**
1. **Shard (Veri Parçaları)** - Gerçek verinin saklandığı MongoDB düğümleridir.
2. **Config Server (Yapılandırma Sunucusu)** - Verinin hangi shard’da bulunduğunu takip eder.
3. **Mongos (Routing Layer)** - İstemcilerden gelen sorguları ilgili shard'a yönlendirir.

---

## 📌 2. Docker Compose ile MongoDB Sharding Kümelenmesi

### **2.1 Docker Compose Dosyası**

**📌 Dosya adı:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  configsvr1:
    image: mongo:latest
    container_name: configsvr1
    command: mongod --configsvr --replSet configReplSet --port 27017
    ports:
      - "27019:27017"
    networks:
      - mongo-cluster

  configsvr2:
    image: mongo:latest
    container_name: configsvr2
    command: mongod --configsvr --replSet configReplSet --port 27017
    networks:
      - mongo-cluster

  configsvr3:
    image: mongo:latest
    container_name: configsvr3
    command: mongod --configsvr --replSet configReplSet --port 27017
    networks:
      - mongo-cluster

  shard1:
    image: mongo:latest
    container_name: shard1
    command: mongod --shardsvr --replSet shardReplSet1 --port 27017
    ports:
      - "27021:27017"
    networks:
      - mongo-cluster

  shard2:
    image: mongo:latest
    container_name: shard2
    command: mongod --shardsvr --replSet shardReplSet2 --port 27017
    ports:
      - "27022:27017"
    networks:
      - mongo-cluster

  shard3:
    image: mongo:latest
    container_name: shard3
    command: mongod --shardsvr --replSet shardReplSet3 --port 27017
    ports:
      - "27023:27017"
    networks:
      - mongo-cluster

  mongos:
    image: mongo:latest
    container_name: mongos
    command: mongos --configdb configReplSet/configsvr1:27017,configsvr2:27017,configsvr3:27017 --port 27017
    ports:
      - "27018:27017"
    networks:
      - mongo-cluster

networks:
  mongo-cluster:
    driver: bridge
```

---

## 📌 3. MongoDB Sharding Yapılandırması

### **3.1 Config Server Replika Setini Başlat**
```sh
docker exec -it configsvr1 mongosh
```

```javascript
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [
    { _id: 0, host: "configsvr1:27017" },
    { _id: 1, host: "configsvr2:27017" },
    { _id: 2, host: "configsvr3:27017" }
  ]
});
```

### **3.2 Shard Replika Setlerini Başlat**

**Shard 1**
```sh
docker exec -it shard1 mongosh
```
```javascript
rs.initiate({
  _id: "shardReplSet1",
  members: [{ _id: 0, host: "shard1:27017" }]
});
```

**Shard 2**
```sh
docker exec -it shard2 mongosh
```
```javascript
rs.initiate({
  _id: "shardReplSet2",
  members: [{ _id: 0, host: "shard2:27017" }]
});
```

**Shard 3**
```sh
docker exec -it shard3 mongosh
```
```javascript
rs.initiate({
  _id: "shardReplSet3",
  members: [{ _id: 0, host: "shard3:27017" }]
});
```

### **3.3 Shard'ları Mongos'a Ekleyelim**
```sh
docker exec -it mongos mongosh
```
```javascript
sh.addShard("shardReplSet1/shard1:27017");
sh.addShard("shardReplSet2/shard2:27017");
sh.addShard("shardReplSet3/shard3:27017");
```

### **3.4 Sharding’i Aktif Etme**
```javascript
sh.enableSharding("ecommerce");
sh.shardCollection("ecommerce.orders", { "customerId": "hashed" });
```

---

## 📌 4. Örnek Veri Ekleme
```javascript
use ecommerce;

for (let i = 1; i <= 1000; i++) {
    db.orders.insertOne({
        customerId: i,
        product: "Ürün " + i,
        amount: Math.floor(Math.random() * 100) + 1
    });
}
```

---

## 📌 5. Hangi Shard’da Olduğunu Bulma
```javascript
db.orders.getShardDistribution();
```

Örnek çıktı:
```
Shard shardReplSet1: 340 documents
Shard shardReplSet2: 330 documents
Shard shardReplSet3: 330 documents
```

---

## 📌 6. Sonuç
✅ **MongoDB Sharding Mimarisi**  
✅ **Docker Compose ile 3 Shard, 3 Config Server ve 1 Mongos Router Kurulumu**  
✅ **Sharding Başlatma ve Konfigürasyonu**  
✅ **Verilerin Shard'lara Dağıtılması**  
✅ **Verinin Hangi Shard'da Olduğunu Bulma**  

🚀 **Artık büyük ölçekli verileri sharding kullanarak dağıtabilir ve yüksek performanslı sorgular çalıştırabilirsin!** 
