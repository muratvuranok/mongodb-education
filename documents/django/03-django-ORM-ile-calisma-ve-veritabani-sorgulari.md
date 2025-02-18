# **Django ORM ile Çalışma ve API Servis Katmanı Kullanımı**

Django'nun **Object-Relational Mapping (ORM)** sistemi, SQL sorgularını Python nesneleriyle yönetmeyi sağlar. **Veritabanı işlemlerini** doğrudan SQL yazmadan gerçekleştirebiliriz. Bu rehberde **Django ORM ile veri ekleme, okuma, güncelleme ve silme işlemlerini API servis katmanı ile ele alacağız.**

---

## **📌 1. Django ORM Kullanımı için Model Tanımlama ve Migration İşlemleri**

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", default=1)
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

## **📌 2. Seed Data (Test Verileri) Ekleme**

📌 **`myapp/services/product_service.py`** dosyanıza ekleyin:

```python
from myapp.models import Product, Category

def seed_data():
    genel_kategori, _ = Category.objects.get_or_create(id=1, name="Genel", description="Genel kategori")
    category1, _ = Category.objects.get_or_create(name="Elektronik", description="Elektronik ürünler")
    category2, _ = Category.objects.get_or_create(name="Giyim", description="Moda ve giyim ürünleri")
    
    Product.objects.bulk_create([
        Product(name="Laptop", description="Yüksek performanslı dizüstü bilgisayar", price=15000.00, stock=10, category=genel_kategori),
        Product(name="Telefon", description="Akıllı telefon", price=8000.00, stock=50, category=genel_kategori),
        Product(name="T-shirt", description="Pamuklu tişört", price=200.00, stock=100, category=genel_kategori)
    ])
```

📌 **Django Shell üzerinden test verilerini ekleyin:**

```sh
python manage.py shell
>>> from myapp.services.product_service import seed_data
>>> seed_data()
```

---

## **📌 3. Serializer Dosyası (API İçin)**

📌 **`myapp/serializers.py`** dosyanıza ekleyin:

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

## **📌 4. API Servis Katmanı (CRUD İşlemleri)**

📌 **`myapp/services/product_service.py`** dosyanıza ekleyin:

```python
from myapp.models import Product, Category
from django.core.exceptions import ObjectDoesNotExist

def get_all_products():
    return Product.objects.select_related('category').all()

def get_product_by_id(product_id):
    try:
        return Product.objects.select_related('category').get(id=product_id)
    except ObjectDoesNotExist:
        return None

def create_product(name, description, price, stock, category_id):
    category = Category.objects.get(id=category_id)
    return Product.objects.create(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category=category
    )

def update_product(product_id, name, description, price, stock, category_id):
    product = get_product_by_id(product_id)
    if product:
        category = Category.objects.get(id=category_id)
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.category = category
        product.save()
        return product
    return None

def delete_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        product.delete()
        return True
    return False
```

---

## **📌 5. URL Yapısı ve API Tanımlamaları**

📌 **`myapp/urls.py`** dosyanıza ekleyin:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
```

📌 **Mevcut URL'leri görmek için:**

```sh
pip install django-extensions
python manage.py show_urls
```

---

## **📌 6. Django Sunucusunu Başlatma ve API’yi Test Etme**

Yaptığınız değişiklikleri uygulamak için sunucuyu başlatın:

```sh
python manage.py runserver
```

**📌 API'yi test etmek için aşağıdaki URL'lere istek atabilirsiniz:**

| **İşlem**   | **URL**            | **Metod** | **Açıklama**            |
| ----------- | ------------------ | --------- | ----------------------- |
| **Listele** | `/api/products/`   | `GET`     | Tüm ürünleri getir      |
| **Ekle**    | `/api/products/`   | `POST`    | Yeni bir ürün ekler     |
| **Detay**   | `/api/products/1/` | `GET`     | Belirli bir ürünü getir |
| **Sil**     | `/api/products/1/` | `DELETE`  | Belirli bir ürünü siler |

🚀 **Şimdi API'yi Postman veya tarayıcıdan test edebilirsin!** 🎯



