# **Using ViewSets and Routers in Django REST Framework (DRF)**

## **📌 Giriş**
Django REST Framework (**DRF**), API geliştirmeyi kolaylaştıran güçlü bir yapıya sahiptir. **ViewSet** ve **Router** bileşenleri, **CRUD işlemlerini** daha kısa ve düzenli bir şekilde tanımlamamızı sağlar.

Bu rehberde **ViewSet ve Router kullanarak API geliştirme sürecini** ele alacağız.

---

## **📌 1. Django REST Framework Kurulumu**
Eğer **DRF** projenizde yüklü değilse, aşağıdaki komut ile yükleyin:

```sh
pip install djangorestframework
```

📌 **`settings.py` içine ekleyin:**

```python
INSTALLED_APPS = [
    ...
    'rest_framework',  # ✅ DRF'yi aktif ettik
]
```

---

## **📌 2. Model Tanımlama**
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

## **📌 3. Serializer Tanımlama**
📌 **`myapp/serializers.py`** dosyanıza aşağıdaki kodu ekleyin:

```python
from rest_framework import serializers
from myapp.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category")

    class Meta:
        model = Product
        fields = "__all__"
```

---

## **📌 4. ViewSet Tanımlama**
📌 **`myapp/views.py`** dosyanıza aşağıdaki kodu ekleyin:

```python
from rest_framework import viewsets
from myapp.models import Product, Category
from myapp.serializers import ProductSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

> **📌 ViewSet kullanımı sayesinde CRUD işlemleri için ayrı ayrı fonksiyon yazmaya gerek kalmaz.**

---

## **📌 5. Router Kullanımı ve URL Yapılandırması**
📌 **`myapp/urls.py`** dosyanıza aşağıdaki kodu ekleyin:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

> **📌 Router, ViewSet'leri otomatik olarak uygun HTTP metodlarıyla eşleştirir.**

---

## **📌 6. API’yi Test Etme**
Django sunucusunu başlatın:

```sh
python manage.py runserver
```

Postman, tarayıcı veya cURL kullanarak API’nizi test edebilirsiniz.

📌 **API İstek Örnekleri:**

| **İşlem**   | **URL**            | **Metod** | **Açıklama**            |
| ----------- | ------------------ | --------- | ----------------------- |
| **Listele** | `/products/`        | `GET`     | Tüm ürünleri getir      |
| **Ekle**    | `/products/`        | `POST`    | Yeni bir ürün ekler     |
| **Detay**   | `/products/1/`      | `GET`     | Belirli bir ürünü getir |
| **Sil**     | `/products/1/`      | `DELETE`  | Belirli bir ürünü siler |

🚀 **Artık Django REST Framework kullanarak ViewSet ve Router ile API oluşturmayı öğrendik!** 🎯

