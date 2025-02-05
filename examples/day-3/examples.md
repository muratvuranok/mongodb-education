# MongoDB Index Kullanımı ve Performans Optimizasyonu

## 1. Veri Ekleme

```javascript
use TestDb;

for(let i = 1000000; i < 1000001000; i++) { 
    db.products.insertOne(
        {
            name: `Product ${i}`,
            category: i % 10 === 0 ? 'Electronics' : 'Clothing',
            price: Math.random() * 1000,
            stock: Math.floor(Math.random() * 100),
            createAt: new Date()
        }
    );
}
```

## 2. İndex Olmadan Sorgulama İşlemi

```javascript
db.products.find({ category: 'Electronics' }).explain('executionStats');
```
**Çıktı:**
- **stage:** 'COLLSCAN' (Collection Scan) → Tüm koleksiyonu tarar.
- **executionTimeMillis:** 1163 ms (Sorgu süresi yüksek olabilir.)

## 3. Tek Alanlı İndeks Kullanımı

```javascript
db.products.createIndex(
    { category: 1 },
    { name: 'category_index' }
);
```

## 4. Bileşik (Compound) İndeks Kullanımı

```javascript
db.products.createIndex(
    { name: -1, category: 1 },
    { name: 'name_category_index' }
);
```

**Örnek Sorgular:**
```javascript
db.products.find({ category: 'Electronics', name: 'Product 1254' }).explain('executionStats');
db.products.find({ category: 'Clothing', name: 'Product 100016' }).explain('executionStats');
```

**Çıktılar:**
- **executionTimeMillis:** 3322 ms → İndeks olmadan sorgu süresi.
- **executionTimeMillis:** 5 ms → İndeks ile optimize edilen sorgu süresi.

## 5. TTL (Time to Live) İndeks Kullanımı

Belirli bir süre sonunda eski kayıtları temizlemek için TTL indeks kullanılır.

```javascript
db.sessions.insertMany([
    { sessionId: 1, user: '1.ahmet', createdAt: new Date() },
    { sessionId: 2, user: '2.ahmet', createdAt: new Date() },
    { sessionId: 3, user: '3.ahmet', createdAt: new Date() },
]);

db.sessions.createIndex(
    { createdAt: 1 },
    { name: 'ttl_index', expireAfterSeconds: 30 }
);
```

## 6. Metin (Text) İndeksi Kullanımı

```javascript
db.products.createIndex(
    { name: 'text', category: 'text' },
    { name: 'name_category_text_index' }
);
```

**Metin Araması:**
```javascript
db.products.find({ $text: { $search: 'Electronics' } }).explain('executionStats');
```

**Çıktı:**
- **nReturned:** 412684 → Dönen kayıt sayısı.
- **executionTimeMillis:** 584 ms → Metin indeksi ile optimize edilen sorgu süresi.
- **indexName:** 'name_category_text_index'.

## 7. OR Operatörü ile Sorgulama

```javascript
db.products.find(
    {
        $or: [
            { name: 'Electronics' },
            { category: 'Electronics' }
        ]
    }
).explain('executionStats');
```

**Çıktı:**
- **executionTimeMillis:** 683 ms
- **nReturned:** 412684

## 8. Sıralama Performansı İçin İndeks

Bir sıralama (sort) işleminde performansı artırmak için indeks ekleyelim.

```javascript
db.products.find({ category: 'Electronics' }).sort({ price: 1 }).explain('executionStats');
```

**Çıktı:**
- **executionTimeMillis:** 1102 ms
- **indexName:** 'category_index'

### Yeni İndeks Ekleyelim

```javascript
db.products.createIndex(
    { price: 1 },
    { name: 'price_index' }
);
```

**Sıralama İşlemi İyileştirildi mi?**

```javascript
db.products.find({ category: 'Electronics' }).sort({ price: 1 }).explain('executionStats');
```

**Çıktı:**
- **executionTimeMillis:** 11976 ms (Daha yavaş oldu! Tekil indeks yerine bileşik indeks kullanmalıyız.)

## 9. Bileşik İndeks ile Sıralama Performansı

```javascript
db.products.createIndex(
    { category: 1, price: 1 },
    { name: 'category_price' }
);
```

**Tekrar Sorgulayalım:**
```javascript
db.products.find({ category: 'Electronics' }).sort({ price: 1 }).explain('executionStats');
```

**Çıktı:**
- **executionTimeMillis:** 1349 ms (Bileşik indeks ile hızlandırıldı.)

## 10. İndeks Kullanımını Zorunlu Hale Getirme (Hint Kullanımı)

```javascript
db.products.find({ category: 'Electronics' }).sort({ price: 1 }).hint('category_index').explain('executionStats');
```

Alternatif kullanım:
```javascript
db.products.find({ category: 'Electronics' }).sort({ price: 1 }).hint({ category: 1 }).explain('executionStats');
```

**Çıktı:**
- **executionTimeMillis:** 853 ms → Optimize edilmiş sorgu süresi.

