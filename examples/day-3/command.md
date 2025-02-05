7wYzWG8Q5ZYgZP5C

MongoDb index türleri 
1. Tekil (single field) indeks
tekil bir alan üzerinde oluşturulan index türüdür, belirli bir alan üzerinde yapılan sorguları hızlanmasını sağlar


db.users.createIndex({ name: 1 }) -> artan sırada (ascending)
db.users.createIndex({ name: -1 }) -> azalan sırada (descending)

db.users.createIndex(
    { 
        fieldName: indexDeğeri(1 / -1) 
    }, 
    {
        name: 'index için bir isim belirleyin'
    }
) -> artan sırada (ascending)



db.users.createIndex({ name: 1 }, {name: 'name_index'}) -> artan sırada (ascending)




2. Bileşik (compound) indeks
birden fazla alanı içeren index türüdür. özellikle belirli alanlar birlikte kullanıluyor ise


// Kullanıcıları adına göre küçükten büyüğe doğru sırala, adı aynı olanları ise, tam tersi sırada sıralama işlemi yap
db.users.createIndex({ name: 1, age: -1 }, { name: 'name_age_index' })


bu indeks şu sorgular için optimize edilir.
name alanına göre yapılan sorgular
name ve age alanına göre yapılan sorgular

db.users.find( { name: 'Ali' } ).explain('executionStats')
db.users.find( { name: 'Ali' , age: { $gt: 25 } } ).explain(''executionStats)
db.users.find( { age: { $gt: 25 } } ).explain('executionStats')





3. Çoklu anahtar (multi key) indeks
bir diziyi (array) içeren alanlara uygulanan indeks türüdür. Dizinin içerisindeki her bir eleman için index oluşturur.


db.movies.createIndex({ genres: 1 }, { name: 'genres_index' }) 
db.movies.find({ genres: 'Comedy' })
 




4. Benzersiz (unique) indeks 
Tekrarlayan (duplicate) değerleri engelleyen indeks türüdür.

db.users.createIndex( 
    { 
        email: 1 
    }, 
    { 
        unique: true, 
        name: 'email_index' 
    }
)
 
db.users.updateOne(
    { name: 'Murat Vuranok' },
    { $set: { name: 'Jon Snowx', email: 'isim@soyisim.com'} },
    { upsert: true }  
)

db.users.find({_id: ObjectId('67a309f0271f391c250d27eb')})
  // -> {upsert:true}   belge yoksa yeni bir belge oluşturacak



db.users.createIndex( { name: 1 },{ name: 'name_unique_index', unique: true } )




5. Metin (text) index
metin bazlı aramalar için kullanılan indeks türüdür. Özellikle (search) işlemlerinde faydalıdır.



db.comments.createIndex( { text: 'text' }, { name: 'comments_text_search_index' } )

/*
 {
    v: 2,                               ->   index versiyonu
    key: { _fts: 'text', _ftsx: 1 },    -> bu bir text index olduğunu gösterr _ftsx: alanı full-text-search (tam metin arama) için kullanır
    name: 'comments_text_search_index',  -> index'in adı
    weights: { text: 1 },               -> index'in ağırlığı  eğer brden fazla alan indexlenmişse, önem sırasına göre ağırlık verilebilir.
    default_language: 'english',        -> varsayılan dil English olarak ayarlanmış
    language_override: 'language',      -> belirli bekgelerede dilin değiştirlmesi için kullanılan alan Eğer bir belge içerisinde `language: "turkish"` gibi bir alan varsa, bu alan turhish dilinde analiz yapılır.
    textIndexVersion: 3   -> indexleme algoritmasının sürümü
  }

*/




db.comments.dropIndex("comments_text_search_index")
db.comments.createIndex(
    {
        text: 'text'
    },
    {
         name: 'comments_text_search_index',
         default_language: 'turkish'
    }
)


6. Küresel (2dsphere) ve Cografi (2d) indekesi
Coğrafi konum bazlı aramalar için kullanılan index. türüdür.



db.places.createIndex( { locaiton: '2dsphere' } )
db.places.find({
    locaion: {
        $near: {
            $geometry: { type: 'Point', coordinates: [40.1782, -74.0051]},
            $maxDistance: 5000 // 5 km içerisinde olanlar
        }
    }
})


7. TTL (Time to Live) indeks
belirli bir süre sonunda otomatik olarak silinmesi gereken belgeler için kullanılır.

db.logs.createIndex( { createAt: 1 }, { expireAfterSeconds: 90 } )

 
mevcut olan indekslerin listelenmesi

db.users.getIndexes()
1  -> artan sırada / ascending
-1 -> azalan sırada / descending

indeks silme işlemi
db.users.dropIndex("index name") -> belirli bir index'i siler
db.users.dropIndexes() -> var olan tüm indeks değerlerini siler


yeni bir index oluşturma
db.users.createIndex({name: 1})


for(let i = 1000000; i < 1000000000; i++){ 
    db.products.insertOne(
        {
            name: `Product ${i}`,
            category: i % 10 === 0 ? 'Electronics': 'Clothing',
            price: Math.random() * 1000,
            stock: Math.floor(Math.random() * 100),
            createAt: new Date()
        }
    ) 
}







zorunlu index kullandırma, sorguda hangi index'in kullanılacağını belirtme

db.users.createIndex({ name: 1, email: -1}, { name: 'name_email_index' })

  { v: 2, key: { email: 1 }, name: 'email_index', unique: true },
  { v: 2, key: { name: 1, email: -1 }, name: 'name_email_index' }

  db.users.find(
    {
        name: 'murat vuranok',
        email: 'isim@soyisim.com'
    },
    {
        _id: 0,
        name: 1,
        email: 1
    }
  ).hint({ name: 1, email: -1 })


    db.users.find(
    {
    name: 'Khal Drogo',
    email: 'jason_momoa@gameofthron.es',
    },
    {
        _id: 0,
        name: 1,
        email: 1
    }
  ).hint('name_email_index')





  