# **Integrating Django ORM with FastAPI**

## **📌 Giriş**
Django ORM, güçlü bir veritabanı yönetim sistemidir ve genellikle Django projeleriyle birlikte kullanılır. Ancak, **FastAPI** ile Django ORM’yi kullanarak veri yönetimini daha esnek hale getirebiliriz.

Bu rehberde **FastAPI içerisinde Django ORM’yi nasıl entegre edeceğimizi** ele alacağız ve **Django veritabanını FastAPI içinde nasıl kullanabileceğimizi** anlatacağız.

---

## **📌 1. Proje Ortamını Hazırlama**
Öncelikle, FastAPI ve Django’yu aynı projede çalıştırmak için gerekli paketleri yükleyelim:

```sh
pip install fastapi uvicorn django djangorestframework psycopg2
```

📌 **Django projesini oluşturun:**

```sh
django-admin startproject mydjango
cd mydjango
python manage.py startapp myapp
```

📌 **`settings.py` içinde `INSTALLED_APPS`’e `myapp` ve `rest_framework` ekleyin:**

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'myapp',
]
```

📌 **Migration işlemlerini çalıştırın:**

```sh
python manage.py makemigrations
python manage.py migrate
```

---

## **📌 2. Django ORM ile Model Tanımlama**
📌 **`myapp/models.py`** dosyanıza aşağıdaki kodu ekleyin:

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

📌 **Migration işlemlerini çalıştırarak modeli veritabanına yansıtın:**

```sh
python manage.py makemigrations myapp
python manage.py migrate
```

---

## **📌 3. FastAPI ile Django ORM’yi Kullanma**
FastAPI’nin Django ORM ile çalışabilmesi için Django ortamını FastAPI’ye dahil etmemiz gerekiyor.

📌 **FastAPI uygulamasını oluşturun:**

📌 **`main.py` dosyası oluşturulacak ve Django projesinin kök dizininde bulunacak:**

```
/myproject
    ├── /mydjango  # Django projesi burası
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
    ├── main.py  # FastAPI uygulaması buraya
```

📌 **`main.py` içeriği:**

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

📌 **FastAPI uygulamasını çalıştırın:**

```sh
uvicorn main:app --reload
```

📌 **FastAPI Çalışırken Django Projesi de Ayakta Olacak mı?**
Evet, Django’nun çalışması gerekiyor çünkü FastAPI, Django’nun ORM’sini kullanıyor. Her iki uygulamayı da aynı anda başlatmalıyız:

```sh
# Terminal 1: Django Sunucusunu Başlat
python manage.py runserver

# Terminal 2: FastAPI Sunucusunu Başlat
uvicorn main:app --reload
```

🚀 **FastAPI artık Django ORM ile entegre çalışıyor!** 🎯

---

## **📌 4. FastAPI Üzerinden CRUD İşlemleri**
Aşağıdaki API isteklerini kullanarak veritabanı işlemlerini gerçekleştirebilirsiniz:

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
    "stock": 100,
    "category_id": 1
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
    "stock": 40,
    "category_id": 1
}
```

### **📌 DELETE - Ürünü Sil**
```sh
DELETE /products/{id}/
```

🚀 **Artık FastAPI ve Django ORM’yi birlikte kullanarak API geliştirebilirsiniz!** 🎯

