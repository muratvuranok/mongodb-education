# MongoDB Security (MongoDB Güvenliği)

## 📌 1. Giriş
MongoDB güvenliği, **erişim kontrolü, şifreleme, ağ güvenliği ve kimlik doğrulama** konularını kapsar.  
Bu rehberde, MongoDB’de **güvenliği sağlamanın en iyi yöntemlerini** öğreneceğiz.

✅ **Öğreneceğimiz konular:**  
- **RBAC (Role-Based Access Control - Rol Bazlı Erişim Kontrolü)**
- **LDAP & Active Directory Entegrasyonu**
- **Field-Level Encryption (Alan Bazlı Şifreleme) ve Client-Side Encryption (İstemci Taraflı Şifreleme)**
- **Network Security ve TLS/SSL Kullanımı**
- **MongoDB Atlas ile IAM Rolleri Yönetme**

---

## 📌 2. RBAC (Role-Based Access Control - Rol Bazlı Yetkilendirme)

MongoDB’de **RBAC (Role-Based Access Control)** mekanizması, **kullanıcı yetkilendirmesini yönetmek için** kullanılır.

### **🔹 2.1 Yeni Bir Kullanıcı Oluşturma**

```javascript
db.createUser({
  user: "appUser",
  pwd: "securePassword123",
  roles: [{ role: "readWrite", db: "ecommerce" }]
});
```

📌 **Bu kullanıcı sadece `ecommerce` veritabanında okuma/yazma iznine sahip olacaktır.**

### **🔹 2.2 Kullanıcıya Yönetici Yetkisi Verme**

```javascript
db.createUser({
  user: "adminUser",
  pwd: "adminSecurePass",
  roles: [{ role: "userAdminAnyDatabase", db: "admin" }]
});
```

✅ **`userAdminAnyDatabase`** rolü, bu kullanıcıya **diğer kullanıcıları yönetme yetkisi** verir.

---

## 📌 3. LDAP & Active Directory Entegrasyonu

Kurumsal ortamlarda **LDAP (Lightweight Directory Access Protocol)** kullanarak MongoDB kullanıcı yönetimini merkezi hale getirebiliriz.

### **🔹 3.1 LDAP ile Kimlik Doğrulama**
MongoDB’yi **LDAP ile entegre etmek** için `mongod.conf` dosyasına aşağıdaki ayarları ekleyebilirsin:

```yaml
security:
  authorization: enabled
  ldap:
    servers: "ldap://ldap.company.com"
    bindDN: "cn=admin,dc=company,dc=com"
    bindPassword: "ldap_admin_pass"
    userToDNMapping: '[{ "match": "(.+)", "substitution": "uid={0},ou=users,dc=company,dc=com" }]'
```

Bu ayar, **LDAP ile MongoDB erişim kontrolü sağlar.**

✅ **LDAP kullanıcıları MongoDB'ye bağlanabilir ve merkezi yetkilendirme yapılabilir.**

---

## 📌 4. Field-Level Encryption ve Client-Side Encryption

MongoDB, **Field-Level Encryption (Alan Bazlı Şifreleme)** ile belirli alanları şifreleyerek **veri güvenliğini artırır**.

### **🔹 4.1 Field-Level Encryption Kullanımı**

MongoDB'de **belirli alanları şifrelemek** için **MongoDB Client-Side Field-Level Encryption (CSFLE)** kullanabiliriz.

✅ **Örnek:** **Kredi kartı bilgilerini şifreleyerek saklama**

```javascript
const schema = {
  bsonType: "object",
  properties: {
    creditCardNumber: {
      encrypt: {
        bsonType: "string",
        algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
      }
    }
  }
};
```

Bu ayar, `creditCardNumber` alanının **şifrelenerek** saklanmasını sağlar.

---

## 📌 5. Network Security ve TLS/SSL Kullanımı

MongoDB'yi güvenli hale getirmek için **TLS/SSL bağlantılarını** etkinleştirmeliyiz.

### **🔹 5.1 TLS/SSL ile Güvenli Bağlantı**

MongoDB **TLS/SSL kullanarak** bağlantıları şifreleyebilir.

✅ **Örnek: `mongod.conf` dosyasında TLS etkinleştirme**

```yaml
net:
  ssl:
    mode: requireSSL
    PEMKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/ca.pem
```

✅ **MongoDB istemcisi ile SSL üzerinden bağlanma:**

```sh
mongo --ssl --host "mongodb.example.com" --sslCAFile /etc/ssl/ca.pem
```

📌 **Bu yapılandırma, MongoDB bağlantılarını şifreleyerek güvenli hale getirir.**

---

## 📌 6. MongoDB Atlas ile IAM Rolleri Yönetme

MongoDB Atlas, **IAM (Identity and Access Management) Rolleri** ile **kullanıcı ve yetki yönetimini** kolaylaştırır.

### **🔹 6.1 Atlas Kullanıcılarına Yetki Verme**

MongoDB Atlas’ta kullanıcı eklerken farklı roller belirleyebilirsin:

```json
{
  "database": "admin",
  "role": "atlasAdmin"
}
```

📌 **`atlasAdmin` rolü, MongoDB Atlas yönetimi için tam yetki sağlar.**

✅ **Alternatif roller:**  
- `readWriteAnyDatabase` → Tüm veritabanlarında okuma/yazma yetkisi  
- `clusterMonitor` → Replika seti ve cluster durumu izleme yetkisi  
- `backup` → Yedekleme yetkisi  

---

## 📌 7. Sonuç

✅ **MongoDB’de güvenlik sağlamak için RBAC kullanmayı öğrendik.**  
✅ **LDAP & Active Directory ile merkezi kimlik doğrulama yaptık.**  
✅ **Field-Level Encryption ile belirli alanları şifreledik.**  
✅ **Network Security için TLS/SSL kullandık.**  
✅ **MongoDB Atlas ile IAM rolleri yönetmeyi öğrendik.**  

🚀 **MongoDB güvenliğini artırarak sistemlerini daha korunaklı hale getirebilirsin!**  
