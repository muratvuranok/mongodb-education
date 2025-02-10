# MongoDB GridFS (Büyük Dosya Saklama)

## 📌 1. GridFS Nedir?
**GridFS**, MongoDB’de **16MB’den büyük dosyaları** saklamak için kullanılan bir sistemdir.  
Büyük dosyaları **küçük parçalara (chunks)** böler ve veritabanında saklar.

📌 **Avantajları:**  
✅ Büyük dosyaları MongoDB’de saklayabiliriz.  
✅ Küçük parçalara bölerek (default 255KB) **performansı artırır**.  
✅ **Streaming desteği sağlar** (dosyaları parça parça okumak mümkün).  
✅ **Paralel yükleme ve indirme desteği** sunar.

---

## 📌 2. GridFS Nasıl Çalışır?

GridFS, dosyaları **iki ayrı koleksiyona** böler:
1. **`fs.files`** → Dosyanın metadata bilgilerini içerir.
2. **`fs.chunks`** → Dosyanın **parçalara bölünmüş veri bloklarını** içerir.

📌 **Dosya Saklama Akışı:**  
✅ Dosya **parçalar halinde (`chunks`)** MongoDB’ye yüklenir.  
✅ Her chunk **`fs.chunks` koleksiyonunda** saklanır.  
✅ Ana dosya bilgileri (`filename, length, uploadDate`) **`fs.files` koleksiyonunda** saklanır.  
✅ Dosya okunurken, **tüm parçalar sırayla birleştirilir ve kullanıcıya döndürülür.**

---

## 📌 3. GridFS Kullanarak Dosya Yükleme ve İndirme

MongoDB’de GridFS ile dosya yönetmek için **Node.js, Python, veya CLI** kullanılabilir.

### **🔹 3.1 MongoDB CLI ile GridFS Kullanımı**

**📌 Dosya Yükleme (`put` komutu ile):**

```sh
mongofiles -d mydatabase put example.jpg
```

**📌 Dosya Listeleme (`list` komutu ile):**

```sh
mongofiles -d mydatabase list
```

**📌 Dosya İndirme (`get` komutu ile):**

```sh
mongofiles -d mydatabase get example.jpg
```

**📌 Dosya Silme (`delete` komutu ile):**

```sh
mongofiles -d mydatabase delete example.jpg
```

📌 **Bu komutlar `fs.files` ve `fs.chunks` koleksiyonlarını otomatik olarak yönetir.**

---

### **🔹 3.2 Node.js ile GridFS Kullanımı**

📌 **Gerekli Kütüphaneyi Yükle:**

```sh
npm install mongodb gridfs-stream
```

📌 **Dosya Yükleme (Upload)**

```javascript
const { MongoClient, GridFSBucket } = require("mongodb");
const fs = require("fs");

async function uploadFile() {
    const client = new MongoClient("mongodb://localhost:27017");
    await client.connect();

    const db = client.db("mydatabase");
    const bucket = new GridFSBucket(db, { bucketName: "files" });

    const uploadStream = bucket.openUploadStream("example.jpg");
    fs.createReadStream("./example.jpg").pipe(uploadStream);

    uploadStream.on("finish", () => {
        console.log("Dosya başarıyla yüklendi!");
        client.close();
    });
}

uploadFile();
```

📌 **Dosya İndirme (Download)**

```javascript
async function downloadFile() {
    const client = new MongoClient("mongodb://localhost:27017");
    await client.connect();

    const db = client.db("mydatabase");
    const bucket = new GridFSBucket(db, { bucketName: "files" });

    const downloadStream = bucket.openDownloadStreamByName("example.jpg");
    downloadStream.pipe(fs.createWriteStream("./downloaded_example.jpg"));

    downloadStream.on("end", () => {
        console.log("Dosya başarıyla indirildi!");
        client.close();
    });
}

downloadFile();
```

📌 **Dosya Silme**

```javascript
async function deleteFile() {
    const client = new MongoClient("mongodb://localhost:27017");
    await client.connect();

    const db = client.db("mydatabase");
    const bucket = new GridFSBucket(db, { bucketName: "files" });

    const file = await db.collection("files.files").findOne({ filename: "example.jpg" });

    if (file) {
        await bucket.delete(file._id);
        console.log("Dosya başarıyla silindi!");
    } else {
        console.log("Dosya bulunamadı!");
    }

    client.close();
}

deleteFile();
```

---

## 📌 4. Chunking Mekanizması (Parçalama)

**GridFS, dosyaları küçük parçalara (chunks) böler.**  
Varsayılan **chunk boyutu 255KB**’dir, ancak değiştirilebilir.

📌 **Örnek:** Eğer **1MB’lık bir dosya yüklersen**:

- **`fs.files` koleksiyonunda 1 kayıt oluşur.**
- **`fs.chunks` koleksiyonunda 4 adet 255KB'lik kayıt oluşur.**

Eğer **chunk boyutunu değiştirmek istiyorsan**:

```javascript
const bucket = new GridFSBucket(db, { bucketName: "files", chunkSizeBytes: 1024 * 512 }); // 512KB
```

---

## 📌 5. GridFS Kullanım Senaryoları

| Senaryo | GridFS Kullanılmalı mı? |
|---------|--------------------|
| Küçük boyutlu belgeler (JSON, text) | ❌ **Hayır, normal MongoDB koleksiyonu daha iyi olur.** |
| 16MB’den büyük dosyalar (PDF, video, resim) | ✅ **Evet, GridFS kullanılması önerilir.** |
| Streaming gerektiren büyük dosyalar | ✅ **Evet, GridFS ile daha verimli olur.** |
| Dosya meta verileri ile ilişkili veritabanı verileri varsa | ✅ **Evet, GridFS verileri ilişkisel yönetebilir.** |
| Sık erişilen küçük dosyalar (HTML, CSS) | ❌ **Hayır, bir CDN veya başka bir çözüm daha uygun olur.** |

---

## 📌 6. Sonuç

✅ **GridFS ile büyük dosyaları MongoDB’de nasıl saklayabileceğimizi öğrendik.**  
✅ **Chunking mekanizması ile verilerin nasıl bölündüğünü gördük.**  
✅ **MongoDB CLI, Node.js kullanarak dosya yükleme, indirme ve silme işlemlerini inceledik.**  
✅ **Hangi durumlarda GridFS kullanmanın uygun olduğunu öğrendik.**  

🚀 **Büyük dosya yönetimi gerektiren projelerde GridFS oldukça güçlü bir çözümdür!**  
