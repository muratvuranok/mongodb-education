# MongoDB Index Türleri

MongoDB'de indeksler, sorguların daha hızlı çalışmasını sağlayan yapılardır. İndeksler, belirli alanlar üzerinde oluşturularak veri tabanı performansını iyileştirir. MongoDB'de farklı indeks türleri mevcuttur.

## 1. Tekil (Single Field) İndeks
Belirli bir alan üzerinde oluşturulan indeks türüdür. Bu indeks, tek bir alan üzerinde yapılan sorguları hızlandırır.

### İndeks Oluşturma
```javascript
db.users.createIndex({ name: 1 }) // Artan sırada (Ascending)
db.users.createIndex({ name: -1 }) // Azalan sırada (Descending)
```

### İndeks Oluşturma ve Ad Belirleme
```javascript
db.users.createIndex(
    { name: 1 }, 
    { name: 'name_index' }
)
```

## 2. Bileşik (Compound) İndeks
Birden fazla alanı içeren indeks türüdür. Bu indeks, belirli alanlar bir arada kullanıldığında sorguları optimize eder.

### İndeks Oluşturma
```javascript
db.users.createIndex({ name: 1, age: -1 }, { name: 'name_age_index' })
```

### Kullanım Senaryoları
Bu indeks aşağıdaki sorguları optimize eder:
```javascript
db.users.find({ name: 'Ali' }).explain('executionStats')
db.users.find({ name: 'Ali', age: { $gt: 25 } }).explain('executionStats')
db.users.find({ age: { $gt: 25 } }).explain('executionStats') // Optimum değil
```

## 3. Çoklu Anahtar (Multi-key) İndeks
Dizi (Array) türündeki veriler için oluşturulur. Dizinin her bir elemanı için indeksleme yapılır.

### İndeks Oluşturma
```javascript
db.movies.createIndex({ genres: 1 }, { name: 'genres_index' })
db.movies.find({ genres: 'Comedy' })
```

## 4. Benzersiz (Unique) İndeks
Aynı alan için tekrar eden (duplicate) değerleri engelleyen indeks türüdür.

### İndeks Oluşturma
```javascript
db.users.createIndex({ email: 1 }, { unique: true, name: 'email_index' })
```

### Kullanım Senaryosu
```javascript
db.users.updateOne(
    { name: 'Murat Vuranok' },
    { $set: { name: 'Jon Snowx', email: 'isim@soyisim.com'} },
    { upsert: true }
)
```

## 5. Metin (Text) İndeksi
Metin bazlı aramalar için kullanılan indeks türüdür. Search (arama) işlemlerini hızlandırır.

### İndeks Oluşturma
```javascript
db.comments.createIndex({ text: 'text' }, { name: 'comments_text_search_index' })
```

### İndeks Silme
```javascript
db.comments.dropIndex("comments_text_search_index")
```

## 6. Küre (2dsphere) ve Coğrafi (2d) İndeksi
Coğrafi konum bazlı aramalar için kullanılan indeks türüdür.

### İndeks Oluşturma
```javascript
db.places.createIndex({ location: '2dsphere' })
```

### Kullanım Senaryosu
```javascript
db.places.find({
    location: {
        $near: {
            $geometry: { type: 'Point', coordinates: [40.1782, -74.0051] },
            $maxDistance: 5000 // 5 km içinde olanlar
        }
    }
})
```

## 7. TTL (Time to Live) İndeksi
Belirli bir süre sonunda otomatik olarak silinmesi gereken belgeler için kullanılır.

### İndeks Oluşturma
```javascript
db.logs.createIndex({ createAt: 1 }, { expireAfterSeconds: 90 })
```

## İndeksleri Listeleme
```javascript
db.users.getIndexes()
```

## İndeks Silme
```javascript
db.users.dropIndex("index_name") // Belirli bir indeksi siler
db.users.dropIndexes() // Tüm indeksleri siler
```

## Belirli Bir İndeksin Kullanılması
Bazen belirli bir indeksin kullanılması zorunlu hale getirilebilir. 

### İndeks Kullanımı
```javascript
db.users.find(
    { name: 'Murat Vuranok', email: 'isim@soyisim.com' },
    { _id: 0, name: 1, email: 1 }
).hint({ name: 1, email: -1 })
```

### Alternatif Kullanım
```javascript
db.users.find(
    { name: 'Khal Drogo', email: 'jason_momoa@gameofthron.es' },
    { _id: 0, name: 1, email: 1 }
).hint('name_email_index')
```

---
Bu belge **Markdown (.md)** formatında kaydedildi ve artık indirilebilir bir hale getirildi.

