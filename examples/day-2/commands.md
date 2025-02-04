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