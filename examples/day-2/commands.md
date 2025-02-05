select sorgusu
db.categories.find() -> select * from categories

NOT: _id default olarak atanmış değeri 1'dir, görünmemesi için 0 olarak işaretlemeniz gerekir.
db.categories.find({},{_id:0, name: 1, description: 1}) -> select name, description from categories


id değerine göre kategori listelenmesi
select * from categories where Id = x
select name, description from categories where Id = x

db.categories.find({_id: ObjectId('67a07d1df969ecfcc00d8190')})
db.categories.find({_id: ObjectId('67a07d1df969ecfcc00d8190')},{
    _id: 0,
    name: 1,
    description: 1
})


delete command
delete from categories -> tüm kategoriler siler ve işimize son verilir.
delete from categories where key = value

db.categories.deleteOne({name: 'yoğun istek üzerine, yeniden güncelledik'})

çoklu kategori silme işlemi
db.categories.deleteMany({name: 'yoğun istek üzerine, yeniden güncelledik'})



like sorguları

kategori tabsolu için, bulk insert

db.categories.insertMany([
    {
        "categoryID": 1,
        "categoryName": "Beverages",
        "description": "Soft drinks, coffees, teas, beers, and ales"
    },
    {
        "categoryID": 2,
        "categoryName": "Condiments",
        "description": "Sweet and savory sauces, relishes, spreads, and seasonings"
    },
    {
        "categoryID": 3,
        "categoryName": "Confections",
        "description": "Desserts, candies, and sweet breads"
    },
    {
        "categoryID": 4,
        "categoryName": "Dairy Products",
        "description": "Cheeses"
    },
    {
        "categoryID": 5,
        "categoryName": "Grains/Cereals",
        "description": "Breads, crackers, pasta, and cereal"
    },
    {
        "categoryID": 6,
        "categoryName": "Meat/Poultry",
        "description": "Prepared meats"
    },
    {
        "categoryID": 7,
        "categoryName": "Produce",
        "description": "Dried fruit and bean curd"
    },
    {
        "categoryID": 8,
        "categoryName": "Seafood",
        "description": "Seaweed and fish"
    }
])


açıklama içerisinde sweet anahtar kelimesi geçen kategorilerin listelenmesi
SELECT * FROM categories WHERE description LIKE '%Sweet%' (contains)
db.categories.find({description: {$regex: /Sweet/}})



categoryName değeri Products ile biten kayıtları listeleyiniz.

db.categories.find({categoryName : { $regex: /ProduCTs/, $options: 'im'}})

'i'
'm'
's'
'x'
'1'


categoryName değeri, con ile başlayan tüm kayıtların listelenmesi
select * from categories where categoryName like 'con%'
select * from categories where LEFT(categoryName,3) = 'con'

db.categories.find({categoryName : {$regex: /^con/, $options: 'i'}})

mongosh "mongodb+srv://cluster0.yuyd0.mongodb.net/" --apiVersion 1 --username muratvuranok
7wYzWG8Q5ZYgZP5C

mongodb+srv://muratvuranok:7wYzWG8Q5ZYgZP5C@cluster0.yuyd0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

mongodb+srv://muratvuranok:7wYzWG8Q5ZYgZP5C@cluster0.yuyd0.mongodb.net/


türü içerisinde, comedy olan filmlerin listelenmesi
db.movies.find({genres: {$in: ['Comedy']}})
db.movies.find({genres: {$in: ['Comedy']}},{_id:0, title:1, genres:1})
db.movies.find({genres: {$in: ['comedy'], $options: 'i'} }) -> hatalı kullanım, $options parametresi sizde regex isteyecektir.
 
db.movies.find(
    {
        genres: {
            $in: ['Comedy']
            $in: [/comedy/i]
        }
    },
    {
        _id:0, 
        title:1, 
        genres:1
    }
)


// aggregations

son 11 yıl içerisinde (2014 sonrası) yapılmış filmlerin ve yorumları
select 
 title,
 genrees,
 etc.  
  
from movies m join comments c on m._id c.movie_id 
as table Test


db.movies.find( 
    {
        year: {$gte:2014}
    } ,
    {
        _id: 0,
        year:1
    }
)


db.movies.aggregate([
    {
        $match: {
            year: {$gte: 2014}
        }
    },
    {
        $lookup: {
            from: "comments",   // comments koleksiyonu ile join yapıyoruz.
            localField: "_id",  // ana koleksiyon (movies) pk alanı
            foreignField: "movie_id", // child koleksiyon içerisindeki fk
            as: "movie_comments"
        }
    },
    {
        $project: {
            _id: 0,
            title: 1,
            year: 1,
            "movie_comments.text": 1,
            "movie_comments.name": 1,
            "movie_comments.email": 1,
        }
    } 
])

NOT:  movies (main collection) içerisindeki _id alanı, db.'dan sonra verdiğiniz tablo için ek bir parametre belirtmenize gerek yoktur.



 Kategorisi western olan filmlerin ortalama süresini hesaplayalım :)


 db.movies.aggregate([
    {
        $match: {
            "year": { $gte: 2014 },
            "genres": { $in: ["Western"] }
        }
    },    
    {
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "movie_id",
            "as": "movie_comments"
        }
    },   
    {
        "$group": {
            "_id": null,
            "avarageDurationTime": { "$avg": "$runtime" },
            "movies": { "$push": "$$ROOT" } 
        }
    },   
    {
       "$project": {
            "_id": 0,
            "avarageDurationTime": 1,
            "movies": {
                "title": 1,
                "genres": 1,
                "year":1,
                "runtime": 1,
                "movie_comments.text": 1,
                "movie_comments.name": 1,
                "movie_comments.email": 1
            }
       }
    }     
 ])

  // $$ROOT -> o anki belgenin tamamını ifade eder.




  select * from products groupby x

  select 
    CategoryName,
    Description,
  P.CategoryID,  -> key
  Count(UnitPrice) as Adet
  
  from Products p join Categories c
  on c.CategoryID = p.CategoryID

  GroupBy P.CategoryID





    türüne göre filmlerin ortalama süresini hesaplama 


db.movies.aggregate([
    {
        "$unwind": { "path": "$genres" }
    },
    {
        "$group": {
            "_id": "$genres",
            "avgTime": { "$avg": "$runtime" }
        }
    },
    {
        "$sort": { "avgTime": -1 }
    }
])

action türünde yer alan filmerin en uzun süreye sahip olan filmi bulunuz (maxTime -> max)

db.movies.aggregate(
[
    {
        "$match": {
            "genres": "Action"
        }
    },
    {
        "$group": {
            "_id": null,
            "maxTime": {
                "$max": "$runtime"
            }
        }
    },
    {
        "$project":{
            "_id": 0,
            "maxTime": 1
        }
    }
])


filmlerin süresini saat ve dakika olarak gösterme



db.movies.aggregate([
    {
       "$addFields": {
            "hours": {
                "$floor": {
                    "$divide": ["$runtime", 60]
                }
            },
            "minutes": {
                "$mod": ["$runtime", 60]
            }
       }
    },
   {
        "$project": {
            "_id": 0,
            "title": 1,
            "runtime": 1,
            "hours": 1,
            "minutes": 1
        }
   }
]) 

// Mongodb Nolock nasıl kullanılır :)
1) $snapshot -> tutarsız okumaları önleme

db.movies.find({ year: {$gte:2014}}).hint({$natural: 1})

 veriyi değiştirme sırasına göre okur, NOLOCK kilitlemeyi kaldırmaz


db.getMongo().startSession(

    {
        readConcern: {
            level : "majority"
        }
    }
)

db.movies.find({ year: {$gte:2014}})



filmlerin süre kategorisine göre sınıflandırma


sure > 120 ? "long" : "short"

db.movies.aggregate([
    {
        "$addFields": {
            "durationCategory": {
                "$cond" : {
                    "if": { $gte: ["$runtime", 120 ]},
                    "then": "long",
                    "else": "short"
                }
            }
        }
    },
    {
        "$sort":{
            "durationCategory": 1
        }
    },
    {
        "$project":{
            "_id":0, 
            "runtime":1,
            "durationCategory":1
        }
    }
])





db.movies.aggregate([ 
    {
        "$project":{
            "_id": 0,  
            "runtime": 1,
            "durationCategory": { 
                "$cond" : {
                    "if": { $gte: ["$runtime", 120 ]},
                    "then": "long",
                    "else": "short"
                }             
            }
        }
    },
    { "$sort":{ "durationCategory": 1 } },
    { "$skip": 5 },
    { "$limit": 5 }
])



 
 





















db.categories.insertMany([
    {   "_id": 1,  "name": "Manav",             "parentId": null  },
    {   "_id": 2,  "name": "Sebzeler",          "parentId": 1  },
    {   "_id": 3,  "name": "Yeşil Sebezeler",   "parentId": 2  },
    {   "_id": 4,  "name": "Kırmızı Sebzeler",  "parentId": 2  },
    {   "_id": 5,  "name": "Meyveler",          "parentId": 1  },
    {   "_id": 6,  "name": "Sarı Meyveler",     "parentId": 5  },
    {   "_id": 7,  "name": "Kırmızı Meyveler",  "parentId": 5  },
    {   "_id": 8,  "name": "Şarkuteri",         "parentId": null  },
    {   "_id": 9,  "name": "Kırmızı Et",        "parentId": 8  },
    {   "_id": 10, "name": "Beyaz Et",          "parentId": 8  },
    {   "_id": 11, "name": "Hindi Et",          "parentId": 8  } 
])


db.categories.aggregate([ 
    {
        $graphLookup: {
            from: "categories",
            startWith: "$_id",
            connectFromField: "_id",
            connectToField: "parentId",
            as: "hierarchy"
        }
    },
    { 
        $project: {
            _id: 1,
            name: 1,
            parentId: 1,
            hierarchy: {
                $map: {
                    input: "$hierarchy",
                    as: "h",
                    in: "$$h.name"
                }
            }
        }
    } 
])