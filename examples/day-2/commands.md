# MongoDB ve SQL Sorgularının Karşılaştırılması

Bu doküman, SQL sorgularının MongoDB karşılıklarını açıklamalar ve kopyalanabilir örneklerle birlikte sunmaktadır.

---

## **1. Tüm Kategorileri Getirme**

### **SQL Sorgusu:**
```sql
SELECT * FROM categories;
```

### **MongoDB Sorgusu:**
```js
db.categories.find()
```

---

## **2. Belirli Alanları Getirme**

### **SQL Sorgusu:**
```sql
SELECT name, description FROM categories;
```

### **MongoDB Sorgusu:**
```js
db.categories.find({}, { _id: 0, name: 1, description: 1 })
```

> **Not:** `_id` alanı varsayılan olarak 1'dir. Eğer görünmemesini istiyorsanız, 0 olarak ayarlamalısınız.

---

## **3. Belirli Bir Kategori Getirme (ID ile)**

### **SQL Sorgusu:**
```sql
SELECT * FROM categories WHERE Id = 'x';
SELECT name, description FROM categories WHERE Id = 'x';
```

### **MongoDB Sorgusu:**
```js
db.categories.find({ _id: ObjectId('67a07d1df969ecfcc00d8190') })
db.categories.find({ _id: ObjectId('67a07d1df969ecfcc00d8190') }, {
    _id: 0,
    name: 1,
    description: 1
})
```

---

## **4. Kategori Silme**

### **SQL Sorgusu:**
```sql
DELETE FROM categories WHERE key = value;
```

### **MongoDB Sorgusu:**
```js
db.categories.deleteOne({ name: 'yoğun istek üzerine, yeniden güncelledik' })
```

> **Not:** `deleteOne()` yalnızca eşleşen ilk kaydı siler.

### **Çoklu Silme (SQL vs MongoDB)**

```sql
DELETE FROM categories WHERE name = 'yoğun istek üzerine, yeniden güncelledik';
```

```js
db.categories.deleteMany({ name: 'yoğun istek üzerine, yeniden güncelledik' })
```

> **Not:** `deleteMany()` tüm eşleşen kayıtları siler.

---

## **5. LIKE Sorguları (Regex ile Kullanım)**

### **Belirli Kelime İçeren Kategoriler (SQL vs MongoDB)**

```sql
SELECT * FROM categories WHERE description LIKE '%Sweet%';
```

```js
db.categories.find({ description: { $regex: /Sweet/ } })
```

### **Belirli Kelime ile Biten Kategoriler**

```sql
SELECT * FROM categories WHERE categoryName LIKE '%Products';
```

```js
db.categories.find({ categoryName: { $regex: /Products$/, $options: 'i' } })
```

### **Belirli Kelime ile Başlayan Kategoriler**

```sql
SELECT * FROM categories WHERE categoryName LIKE 'Con%';
```

```js
db.categories.find({ categoryName: { $regex: /^Con/, $options: 'i' } })
```

| **Parametre** | **Açıklama** |
|--------------|-------------|
| `i` | Büyük/küçük harf duyarlılığını kaldırır. |
| `m` | Çok satırlı (multiline) arama yapar. |
| `s` | `.` karakterinin yeni satır (`\n`) ile eşleşmesini sağlar. |
| `x` | Regex içinde boşlukları görmezden gelir. |

---

## **6. Belirli Türdeki Filmleri Getirme**

### **SQL Sorgusu:**
```sql
SELECT * FROM movies WHERE genres IN ('Comedy');
```

### **MongoDB Sorgusu:**
```js
db.movies.find({ genres: { $in: ['Comedy'] } })
db.movies.find({ genres: { $in: ['Comedy'] } }, { _id: 0, title: 1, genres: 1 })
```

> **Not:** `$in` operatörü, belirli bir değerin dizi içinde olup olmadığını kontrol eder.

---

## **7. Aggregation: Son 10 Yıldaki Filmleri ve Yorumları Listeleme**

### **SQL Sorgusu:**
```sql
SELECT m.title, m.year, c.text, c.name, c.email
FROM movies m
JOIN comments c ON m._id = c.movie_id
WHERE m.year >= 2014;
```

### **MongoDB Sorgusu:**
```js
db.movies.aggregate([
    { $match: { year: { $gte: 2014 } } },
    { $lookup: {
        from: 'comments',
        localField: '_id',
        foreignField: 'movie_id',
        as: 'movie_comments'
    }},
    { $project: {
        _id: 0,
        title: 1,
        year: 1,
        'movie_comments.text': 1,
        'movie_comments.name': 1,
        'movie_comments.email': 1
    }}
])
```

> **Not:** `$lookup`, SQL'deki `JOIN` işlemiyle aynıdır.

---

## **8. Kategorisi 'Western' Olan Filmlerin Ortalama Süresini Hesaplama**

### **SQL Sorgusu:**
```sql
SELECT AVG(runtime) AS averageDurationTime
FROM movies
WHERE year >= 2014 AND genres LIKE '%Western%';
```

### **MongoDB Sorgusu:**
```js
db.movies.aggregate([
    { $match: { year: { $gte: 2014 }, genres: { $in: ['Western'] } } },
    { $group: { _id: null, averageDurationTime: { $avg: '$runtime' } } },
    { $project: { _id: 0, averageDurationTime: 1 } }
])
```

> **Not:** `$avg`, belirtilen alandaki değerlerin ortalamasını alır.

---

Bu doküman, MongoDB ve SQL sorgularının karşılaştırmalarını içermektedir. Kullanımınıza göre düzenlemeler yapabilirsiniz!
