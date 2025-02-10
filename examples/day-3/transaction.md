# MongoDB Transactions Kullanımı (Replica Set veya Sharded Cluster Gerektirir)

MongoDB'de **transactions (işlemler)**, birden fazla koleksiyon üzerinde **atomik işlemler** gerçekleştirmek için kullanılır. Transactions kullanımı için **Replica Set** veya **Sharded Cluster** ortamı gereklidir.

## 1. Kullanıcı ve Hesap Bilgisi Ekleme

```javascript
db.accounts.insertOne({
    userName: '1.Murat',
    balance: 1000
});
```

## 2. Transaction Kullanarak Güncelleme ve İşlem Ekleme

```javascript
const session = db.getMongo().startSession();  // Session başlat
session.startTransaction();   // Transaction başlat

try {
    const dbTest = session.getDatabase('TestDb'); // Session bağlı veritabanını al

    // accounts koleksiyonunda yer alan verileri güncelleyelim
    const updateResult = dbTest.accounts.updateOne(
        { userName: '2.Murat' }, // Kullanıcı adı doğru yazılmalı
        { $inc: { balance: -500 } },
        { session }
    );

    // Eğer kullanıcı bulunamazsa işlemi iptal et
    if (updateResult.matchedCount === 0) {
        throw new Error('Kullanıcı bulunamadı veya güncelleme başarısız.');
    }

    // transactions koleksiyonuna yeni bir işlem ekleme
    dbTest.transactions.insertOne(
        {
            userName: '2.Murat',
            type: 'withdraw',
            amount: 500,
            date: new Date()
        },
        { session }
    );

    session.commitTransaction(); // İşlemi onayla ve kaydet
    console.log('Transaction başarıyla tamamlandı.');
} catch (error) {
    session.abortTransaction();  // İşlem başarısız olursa geri al (rollback)
    console.error('Transaction geri alındı:', error);
} finally {
    session.endSession(); // Session'ı kapat
}
```

## 3. Transactions İçin Gereksinimler
- Transactions kullanımı için **Replica Set** veya **Sharded Cluster** yapılandırması gereklidir.
- **Standalone MongoDB instance** üzerinde transactions çalışmaz.
- İşlemler **MongoDB 4.0** ve üstü sürümlerde desteklenmektedir.

## 4. Replica Set Ayarları
Transactions'ı kullanabilmek için MongoDB'yi **Replica Set** olarak başlatmanız gerekmektedir.

```bash
mongod --replSet myReplicaSet --bind_ip localhost
```

Ardından, MongoDB kabuğunda **Replica Set**'i başlatın:

```javascript
rs.initiate()
```

## 5. Sharded Cluster Ayarları
Eğer sharded cluster üzerinde çalışıyorsanız, **transactions**'ı destekleyen bir yapılandırma gereklidir.

```bash
mongos --configdb configReplSet/localhost:27019 --bind_ip localhost
```

Ardından, **Shard ekleyin:**

```javascript
sh.addShard("shard1/localhost:27018")
```

## 6. Transaction ile İlgili Önemli Notlar
- **Multi-Document Transactions** işlemleri tek bir ACID uyumlu işlem olarak yürütülür.
- **Write Concern:** Eğer veriler belirli bir sayıda node'a yazılmadan işlemi tamamlamak istemiyorsanız, **writeConcern** opsiyonu kullanılabilir.
- **Durum Kontrolleri:** Transaction sırasında hata yönetimi için `matchedCount` ve `modifiedCount` gibi değerler kontrol edilmelidir.

Bu yapılandırma sayesinde MongoDB transactions ile güvenli ve tutarlı işlemler gerçekleştirebilirsiniz.

