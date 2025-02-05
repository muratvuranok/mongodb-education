
db.accounts.insertOne({
    userName: '1.Murat',
    balance: 1000
})

const session = db.getMongo().startSession();  // Session başlat
session.startTransaction();   // Transaction başlat

try {
    // accounts koleksiyonunda yer alan verileri güncelleyelim
    const updateResult = session.getDatabase('TestDb').accounts.updateOne(
        { username: '2.Murat' }, // Doğru alan adını kontrol et
        { $inc: { balance: -500 } },
        { session }
    );

    // Eğer kullanıcı bulunamazsa işlemi iptal et
    if (updateResult.matchedCount === 0) {
        throw new Error('Kullanıcı bulunamadı veya güncelleme başarısız.');
    }

    // transactions koleksiyonuna yeni bir işlem ekleme
    session.getDatabase('TestDb').transactions.insertOne(
        {
            username: '2.Murat',
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


// replica set veya sharded cluster