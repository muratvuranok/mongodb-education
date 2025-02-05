use TestDb

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


index olmadan sorgulama işlemi
db.products.find( {category : 'Electronics' } ).explain('executionStats')

stage: 'COLLSCAN'         -> (collection scan) tüm koleksiyonu tarar
executionTimeMillis: 1163  -> kaç ms arama işlemini yaptı


db.products.createIndex(
    {
        category : 1
    },
    {
        name: 'category_index'
    }
)



birleşik index kullanımı

db.products.find( { category : 'Electronics' , name: 'Product 1254'} ).explain('executionStats')
db.products.find( { category : 'Clothing' , name: 'Product 100016'} ).explain('executionStats')


    executionTimeMillis: 3322
    executionTimeMillis: 5,   

db.products.find({}).skip(100000)


db.products.createIndex( { name : -1, category: 1 }, { name: 'name_category_index' })


TTL indeks kullanımı

createIndex alanına bağlı olarak eski kayıtları otomatik olarak temizlemek için bir TTL index kullanabilirsiniz.



db.sessions.insertMany(
    [
        { sessionId: 1, user: '1.ahmet', createdAt: new Date() },
        { sessionId: 2, user: '2.ahmet', createdAt: new Date() },
        { sessionId: 3, user: '3.ahmet', createdAt: new Date() },
        { sessionId: 4, user: '4.ahmet', createdAt: new Date() },
        { sessionId: 5, user: '5.ahmet', createdAt: new Date() },
        { sessionId: 6, user: '6.ahmet', createdAt: new Date() },
        { sessionId: 7, user: '7.ahmet', createdAt: new Date() },
        { sessionId: 8, user: '8.ahmet', createdAt: new Date() },
    ]
)

db.sessions.createIndex( { createdAt: 1 }, { name: 'ttl_index', expireAfterSeconds: 30 } )


db.products.find()  
db.products.createIndex( {name: 1 })
db.products.createIndex( {name: -1 })



db.products.createIndex( { name: 'text', category: 'text' }, { name: 'name_category_text_index' })



select * from categories where name = 'Electronics' and category = 'Electronics'
select * from categories where name = 'Electronics' or category = 'Electronics'


db.products.find( { name: 'Electronics', category: 'Electronics' } ).explain('executionStats')







db.products.find( { $text: { $search: 'Electronics' } } ).explain('executionStats')
   
nReturned: 412684,
executionTimeMillis: 584,
filter: { '$text': { '$search': 'Electronics' } },
indexName: 'name_category_text_index',





db.products.find(
    {
        $or: [
            { name: 'Electronics' },
            { category: 'Electronics' },
        ]
    },
).explain('executionStats')

executionTimeMillis: 683,
nReturned: 412684,


sıralama performansı için index

bir sıralama sorgusunda (sort) performansını iyileştirmek için price alanına index ekleyelim.

db.products.find( { category: 'Electronics' } ).sort( { price: 1} ).explain('executionStats')
   executionTimeMillis: 1102,
   indexName: 'category_index',

db.products.createIndex( { price: 1 }, { name: 'price_index' })


   executionTimeMillis: 11976,
     indexName: 'price_index',


bileşik index'e geçiş :)

db.products.createIndex(
    {
        category: 1,
        price: 1
    },
    {
        name: 'category_price'
    }
)

    executionTimeMillis: 1349,


db.products.find( { category: 'Electronics' } ).sort( { price: 1} ).hint('category_index').explain('executionStats')

db.products.find( { category: 'Electronics' } ).sort( { price: 1} ).hint({ category: 1 }).explain('executionStats')


 executionTimeMillis: 853