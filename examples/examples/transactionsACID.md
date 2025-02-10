# MongoDB Transactions & ACID Support (MongoDB'de Transaction Kullanımı)

## 📌 1. MongoDB'de ACID Desteği Var mı?
MongoDB, **4.0 sürümünden itibaren ACID (Atomicity, Consistency, Isolation, Durability) uyumlu çok belgeli (multi-document) işlemleri destekler**.  

MongoDB'nin **tek doküman (single document) işlemleri** zaten **ACID garantisi sağlar**. Ancak, **multi-document transactions** özelliği ile **birden fazla dokümanda işlem yaparken tüm işlemleri bir bütün halinde yönetebiliriz**.

---

## 📌 2. Multi-Document Transactions (Çoklu Doküman İşlemleri)
**Transactions**, birden fazla belge üzerinde değişiklik yaparken **ya hep ya hiç (all-or-nothing)** prensibiyle çalışır.

🔹 **MongoDB'de transaction desteği sadece replika setleri ve sharded cluster’lar üzerinde çalışır.**  

✅ **Örnek: Banka transferi işlemi**  
Bir kullanıcının başka bir kullanıcıya para göndermesini sağlayan işlemi düşünelim. Bu işlem iki adımda gerçekleşir:
1. Gönderen hesabın bakiyesi düşürülür.
2. Alıcı hesabın bakiyesi artırılır.
3. Eğer biri başarısız olursa, işlem geri alınır (rollback).

---

## 📌 3. Session ve Transaction API Kullanımı

### **🔹 3.1 MongoDB'de Transaction Başlatma**
MongoDB’de **transactions**, bir **session (oturum) içinde** başlatılır.

```javascript
const session = db.getMongo().startSession();
session.startTransaction();

try {
    db.accounts.updateOne(
        { _id: "user1" },
        { $inc: { balance: -100 } },
        { session }
    );

    db.accounts.updateOne(
        { _id: "user2" },
        { $inc: { balance: 100 } },
        { session }
    );

    session.commitTransaction(); // İşlemi tamamla
} catch (error) {
    session.abortTransaction(); // Hata olursa geri al
}

session.endSession();
```

📌 **Bu işlem ya tamamen başarılı olur ya da tamamen iptal edilir.**  

---

### **🔹 3.2 Transaction'ın Başarı Durumunu Kontrol Etme**
**Eğer transaction başarılı olduysa**, commit edilir. Eğer bir hata olursa, rollback yapılır.

```javascript
const session = db.getMongo().startSession();
session.startTransaction();

try {
    db.orders.insertOne(
        { _id: "order123", product: "Laptop", price: 2000 },
        { session }
    );

    db.payments.insertOne(
        { _id: "payment123", order_id: "order123", status: "Paid" },
        { session }
    );

    session.commitTransaction();
    print("Transaction başarılı!");
} catch (error) {
    session.abortTransaction();
    print("Transaction başarısız oldu, geri alındı.");
}

session.endSession();
```

**⚠️ Dikkat:** Eğer ikinci `insertOne` başarısız olursa, **ilk işlem de geri alınacaktır.**

---

## 📌 4. Write Concern ve Read Concern Kavramları
MongoDB’de **veri yazma ve okuma işlemlerinin güvenliği için** `Write Concern` ve `Read Concern` mekanizmaları kullanılır.

### **🔹 4.1 Write Concern (Yazma Güvenliği)**
**Write Concern**, bir işlemin tamamlandığından emin olmak için **kaç düğümün (node) işlemi onaylaması gerektiğini belirler**.

| Write Concern | Açıklama |
|--------------|---------|
| `{ w: 1 }` | Tek bir düğüm yazmayı onaylarsa tamamlanır (varsayılan) |
| `{ w: "majority" }` | Çoğunluk düğüm yazmayı onaylamadan işlem tamamlanmaz |
| `{ w: 0 }` | Yazma işlemi onaysız çalışır (en hızlı ama en az güvenli yöntem) |

✅ **Örnek:** Majoriyete yazma garantisi olan bir işlem

```javascript
db.orders.insertOne(
    { order_id: "A123", total: 100 },
    { writeConcern: { w: "majority", j: true, wtimeout: 2000 } }
);
```

- **`j: true`** → Verinin diske yazıldığını garanti eder.
- **`wtimeout: 2000`** → 2 saniyede çoğunluk onay vermezse hata döndür.

---

### **🔹 4.2 Read Concern (Okuma Güvenliği)**
**Read Concern**, verinin ne kadar güvenli bir şekilde okunacağını belirler.

| Read Concern | Açıklama |
|--------------|---------|
| `{ level: "local" }` | En hızlı, ancak en az güvenli okuma |
| `{ level: "majority" }` | Çoğunluk düğümlerden onaylanmış veriyi döndürür |
| `{ level: "linearizable" }` | Dağıtık sistemlerde en güçlü garanti sağlar |

✅ **Örnek:** Majority Read Concern Kullanımı

```javascript
db.orders.findOne({ order_id: "A123" }, { readConcern: { level: "majority" } });
```

📌 **Bu, sadece çoğunluk düğümler tarafından onaylanmış verileri döndürür.**

---

## 📌 5. İşlemler Sırasında Deadlock ve Hata Yönetimi

### **🔹 5.1 Deadlock (Kilitleme) Sorunu**
**Transaction’lar sırasında iki işlem aynı kaynağı beklerse "Deadlock" oluşabilir.**

🛑 **Örnek Deadlock Senaryosu:**
1. **İşlem 1**: Kullanıcı A’dan B’ye para transfer ediyor.
2. **İşlem 2**: Kullanıcı B’den A’ya para transfer ediyor.

💡 **Çözüm:** **İşlemleri sıralı yap veya zaman aşımları kullan.**

```javascript
session.startTransaction({ readConcern: { level: "snapshot" } });
```

**Snapshot isolation**, deadlock ihtimalini azaltır.

---

## 📌 6. Sonuç
✅ **MongoDB’nin ACID desteğini öğrendik.**  
✅ **Multi-document transaction işlemlerini inceledik.**  
✅ **Session ve Transaction API’sini kullandık.**  
✅ **Write Concern ve Read Concern kavramlarını öğrendik.**  
✅ **Deadlock ve hata yönetimi için önlemleri inceledik.**  

🚀 **Artık MongoDB üzerinde güvenli ve sağlam transaction işlemleri yapabilirsin!**  
