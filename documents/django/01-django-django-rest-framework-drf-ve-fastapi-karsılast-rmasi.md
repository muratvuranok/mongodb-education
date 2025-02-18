# **Django, Django REST Framework (DRF) ve FastAPI Karşılaştırması**

## **📌 Django Nedir?**
Django, **Python ile yazılmış, açık kaynaklı, yüksek seviyeli bir web framework'üdür**. **Hızlı geliştirme** ve **temiz, pragmatik tasarım** için geliştirilmiştir. Django'nun amacı, **tekrarlanan görevleri otomatize ederek geliştiricinin daha hızlı ve verimli kod yazmasını sağlamak**tır.

### **✅ Django'nun Avantajları**
- **MVT (Model-View-Template) yapısı** ile düzenli ve sürdürülebilir kod yazımı sağlar.
- **ORM (Object-Relational Mapping)** ile SQL kullanmadan veritabanı yönetimi yapabiliriz.
- **Güvenlik** konusunda güçlüdür, CSRF, XSS, SQL Injection gibi saldırılara karşı koruma sağlar.
- **Admin paneli** sayesinde verileri yönetmek için ek bir panel geliştirmeye gerek yoktur.
- **Esneklik ve geniş ekosistem** ile farklı ihtiyaçlara uygun paketler bulunur.

---

## **📌 Django REST Framework (DRF) Nedir?**
**Django REST Framework (DRF), Django ile API (Application Programming Interface) geliştirmeyi kolaylaştıran güçlü bir eklentidir.** DRF sayesinde, **RESTful API'ler hızlı ve verimli bir şekilde oluşturulabilir.**

### **✅ Django REST Framework'ün Avantajları**
- **ModelSerializer** sayesinde veri modellemesi ve JSON dönüşümleri kolaylaşır.
- **Authentication & Authorization** mekanizmaları sayesinde güvenli API geliştirme imkanı sunar.
- **ViewSets & Routers** ile CRUD işlemleri hızlıca oluşturulabilir.
- **Class-Based Views (CBV) & Function-Based Views (FBV)** desteği ile esneklik sağlar.
- **Browsable API** sayesinde tarayıcı üzerinden API'yi test etme imkanı sunar.

---

## **📌 Django ve FastAPI Karşılaştırması**
Django ve FastAPI, **web geliştirme için kullanılan iki güçlü framework'tür**, ancak kullanım amaçları farklıdır.

### **🚀 Django vs FastAPI Kullanım Senaryoları**
| **Özellik**              | **Django + DRF** | **FastAPI** |
|--------------------------|-----------------|------------|
| **Genel Kullanım**       | Web Uygulamaları, REST API'ler | Mikroservisler, API geliştirme |
| **Hız ve Performans**    | Daha yavaş (Senkrondur) | Daha hızlı (Asenkron destekli) |
| **Otomatik Admin Paneli**| ✅ | ❌ |
| **ORM (Veritabanı Yönetimi)** | ✅ (Django ORM) | ✅ (SQLAlchemy / Tortoise ORM) |
| **Asenkron Destek**      | Kısıtlı | Tam asenkron destek |
| **Dokümantasyon**        | Manüel | Otomatik OpenAPI/Swagger |
| **WebSockets Desteği**   | Channels ile | Doğrudan desteklenir |

---

# **📌 Django Projesi Kurulumu ve Model Oluşturma**

## **✅ Django Projesi Başlatma**
Öncelikle, yeni bir Django projesi başlatmak için aşağıdaki komutu çalıştırın:
```sh
pip install django
```

Projeyi oluşturmak için:
```sh
django-admin startproject myproject
cd myproject
python manage.py migrate
python manage.py runserver
```

Bu işlemlerden sonra `http://127.0.0.1:8000/` adresine giderek Django’nun çalıştığını görebilirsiniz.

---

## **✅ Django Uygulaması (App) Oluşturma**
Django projesi içinde bir uygulama oluşturmak için şu komutu çalıştırın:
```sh
python manage.py startapp myapp
```
Oluşan klasör yapısı şu şekildedir:
```
myproject/
│── myapp/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
```

**myapp'ı projemize eklemek için `settings.py` dosyasına ekleyin:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
```

---

## **✅ Django Model Tanımlama**
Django ORM kullanarak model tanımlamak için **`models.py`** dosyanıza aşağıdaki örneği ekleyin:

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

Modeli veritabanına eklemek için **migration işlemlerini** yapın:
```sh
python manage.py makemigrations
python manage.py migrate
```

Böylece **Category** modeli veritabanına eklenmiş olur.

---

## **📌 Sonuç**
✅ Django projesi kuruldu ve çalıştırıldı.  
✅ Django uygulaması (`myapp`) oluşturuldu.  
✅ Model (`Category`) tanımlandı ve veritabanına eklendi.  
✅ Django ORM kullanılarak modelleme yapıldı.

🚀 **Bir sonraki adımda Django REST Framework ile API oluşturmaya geçeceğiz!** 🎯

