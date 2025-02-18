# **Building a Hybrid Project Using Django for Database and FastAPI for APIs**

## **📌 Giriş**
Django, güçlü bir **veritabanı yönetimi ve ORM (Object-Relational Mapping) sistemi** sunarken, **FastAPI**, yüksek performanslı API servisleri geliştirmek için idealdir. Bu rehberde, **Django’yu veritabanı yönetimi için kullanarak, API servislerini FastAPI ile nasıl oluşturabileceğimizi** adım adım öğreneceğiz.

---

## **📌 1. Proje Yapısını Belirleme**
Öncelikle **Django** ve **FastAPI** bileşenlerini içeren bir proje yapısı oluşturmalıyız.

📌 **Proje Klasör Yapısı:**
```
/hybrid_project
    ├── /mydjango  # Django Projesi
    │   ├── mydjango/
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── wsgi.py
    │   │   ├── asgi.py
    │   ├── myapp/
    │   │   ├── models.py
    │   │   ├── views.py
    │   │   ├── serializers.py
    ├── main.py  # FastAPI Uygulaması
```

---

## **📌 2. Gerekli Paketleri Yükleme**
Öncelikle Django ve FastAPI’nin birlikte çalışması için gerekli paketleri yükleyelim.

```sh
pip install django djangorestframework fastapi uvicorn psycopg2
```

📌 **Django projesini başlatın:**
```sh
django-admin startproject mydjango
cd mydjango
python manage.py startapp myapp
```

📌 **Django uygulamasını konfigüre edin:**
`settings.py` dosyanıza şu uygulamaları ekleyin:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp',
]
```

📌 **Veritabanı migration işlemlerini yapın:**
```sh
python manage.py makemigrations
python manage.py migrate
```

---

## **📌 3. Django ORM ile Model Tanımlama**
📌 **`myapp/models.py` dosyanıza aşağıdaki modeli ekleyin:**

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

📌 **Migration işlemlerini yaparak modeli veritabanına kaydedin:**
```sh
python manage.py makemigrations myapp
python manage.py migrate
```

---

## **📌 4. FastAPI ile API Servisi Oluşturma**
Şimdi Django veritabanını kullanarak FastAPI üzerinde API servislerini oluşturacağız.

📌 **`main.py` dosyanızı oluşturun:**

```python
import os
import django
from fastapi import FastAPI, Depends
from django.db import connection
from myapp.models import Product

# Django ayarlarını yükle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")
django.setup()

app = FastAPI()

def get_db():
    return connection

@app.get("/products/")
def get_products(db=Depends(get_db)):
    products = Product.objects.all()
    return [{"id": p.id, "name": p.name, "price": p.price} for p in products]
```

📌 **FastAPI uygulamasını başlatın:**
```sh
uvicorn main:app --reload
```

📌 **Django uygulamasını da aynı anda başlatın:**
```sh
python manage.py runserver
```

🚀 **Artık FastAPI, Django ORM ile birlikte API servisi sağlayabiliyor!**

---

## **📌 5. FastAPI Üzerinden CRUD İşlemleri**
Aşağıdaki API isteklerini kullanarak veri yönetimini gerçekleştirebilirsiniz.

### **📌 GET - Tüm Ürünleri Getir**
```sh
GET /products/
```
📌 **Yanıt Örneği:**
```json
[
    {"id": 1, "name": "Laptop", "price": 15000.00},
    {"id": 2, "name": "Telefon", "price": 8000.00}
]
```

### **📌 POST - Yeni Ürün Ekle**
```sh
POST /products/
Content-Type: application/json
```
📌 **İstek Gövdesi:**
```json
{
    "name": "T-shirt",
    "description": "Pamuklu tişört",
    "price": 200.00,
    "stock": 100
}
```

### **📌 GET - Belirli Bir Ürünü Getir**
```sh
GET /products/{id}/
```

### **📌 PUT - Ürünü Güncelle**
```sh
PUT /products/{id}/
Content-Type: application/json
```
📌 **İstek Gövdesi:**
```json
{
    "name": "Akıllı Telefon",
    "description": "Yüksek kaliteli telefon",
    "price": 8500.00,
    "stock": 40
}
```

### **📌 DELETE - Ürünü Sil**
```sh
DELETE /products/{id}/
```

🚀 **Artık Django ve FastAPI'yi birlikte kullanarak yüksek performanslı API'ler geliştirebilirsiniz!** 🎯

