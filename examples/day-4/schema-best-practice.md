
# MongoDB İlişkisel Veri Modelleme

## **1. Embedded Kullanım**
```json
{ 
    "_id": 1,
    "name": "Murat Vuranok",
    "orders": [ 
        { "order_id": 101, "total": 50.0, "date": "2024-02-05" },
        { "order_id": 102, "total": 30.0, "date": "2024-02-06" }
    ]
}
```

## **2. Referenced Kullanım**
```json
{ 
    "_id": 1,
    "name": "Murat Vuranok",
    "orders": [101, 102]
}
{ 
    "_id": 101, 
    "customer_id": 1,
    "total": 50.0, 
    "date": "2024-02-05"  
}
```

## **3. One to One - Embedded Kullanım**
```json
{ 
    "_id": 1,
    "name": "Murat Vuranok",
    "profile": {
        "age": 43,
        "email": "isim@soyisim.com"
    }
}
```

## **4. One to One - Referenced Kullanım**
```json
{ 
    "_id": 1,
    "name": "Murat Vuranok",
    "profile_id": 101
}
{
    "_id": 101,
    "user_id": 1,
    "age": 43,
    "email": "isim@soyisim.com"
}
```

## **5. One to Many - Embedded Kullanım**
```json
{ 
     "_id": 1,
     "name": "laptop",
     "reviews": [
        { "user": "ali", "rating": 5, "comment": "Harika!" },
        { "user": "ayşe", "rating": 4, "comment": "Fena değil!" }
     ]
} 
```

## **6. One to Many - Referenced Kullanım**
```json
{ 
     "_id": 1,
     "name": "laptop"
}

{
    "_id": 101,
    "product_id": 1,
    "user": "ali",
    "comment": "Harika",
    "rating": 5
}
```

## **7. Many to Many Kullanımı**
```json
{ 
     "_id": 1,
     "name": "Murat",
     "roles": [ 101, 102 ]
} 

{
    "_id": 101,
    "user_id": 1,
    "role": "admin"
}
```

## **8. One to One MongoDB Sorguları**
```json
db.users.insertMany([
    {
        "name": "murat vuranok",
        "email": "isim@soyisim.com",
        "profile": {
            "address": "istanbul",
            "phone": "1234567890"
        }
    }
])
```

## **9. One to Many MongoDB Sorguları**
```json
db.customers.insertMany([
    {
        "_id": 1,
        "name": "murat vuranok",
        "email": "isim@soyisim.com",
        "orders": [
            {
                "order_date": "2020-01-01",
                "total": 100
            },
            {
                "order_date": "2020-01-02",
                "total": 200
            }
        ]
    }
])
```

## **10. Many to Many MongoDB Sorguları**
```json
db.ogrenciler.aggregate(
    [
        {
            $lookup: {
                from: 'student_courses',
                localField: '_id',
                foreignField: 'student_id',
                as: 'student_courses'
            }
        },
        {
            $unwind: '$student_courses' 
        },
        {
            $lookup: {
                from: 'dersler',
                localField: 'student_courses.course_id',
                foreignField: '_id',
                as: 'course_detail'
            }
        },
        {
            $unwind:   '$course_detail' 
        },
        {
            $project: { 
                name: 1, 
                'course_detail.name': 1
            }
        } 
    ]
)
``` 