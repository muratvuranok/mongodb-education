# **Django Admin Paneli ve Django REST Framework (DRF) ile API CRUD İşlemleri**

Django’nun **Admin Paneli**, verileri yönetmek için güçlü bir araçtır. **CRUD (Create, Read, Update, Delete) işlemlerini hızlıca gerçekleştirmek** için admin panelini kullanabiliriz. Bu rehberde, **Django Admin Paneli'ni etkinleştirecek, modele kaydedecek ve Django REST Framework (DRF) ile API CRUD işlemlerini yöneteceğiz.**

---

## **📌 1. Django REST Framework'ü (DRF) Kurma ve Tanıtma**
Öncelikle Django REST Framework’ü yükleyelim:

```sh
pip install djangorestframework
```

Daha sonra **DRF’yi projemize tanıtalım**. 📌 **`settings.py`** dosyanızı açın ve `INSTALLED_APPS` içine `rest_framework` eklediğinizden emin olun:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # DRF buraya eklendi
    'myapp',  # Uygulamanız
]
```

Bu adımları tamamladıktan sonra sunucunuzu yeniden başlatın:

```sh
python manage.py runserver
```

DRF artık aktif ve kullanılabilir! 🚀

---

## **📌 2. Django Admin Panelini Etkinleştirme**
Django, admin panelini **varsayılan olarak** sağlar. Eğer projenizi kurduysanız, aşağıdaki komutla admin paneline erişebilirsiniz:

```sh
python manage.py createsuperuser
```
Bu komut çalıştırıldığında, **kullanıcı adı, e-posta ve şifre** belirlemeniz istenecektir.

Daha sonra, Django Admin Paneline giriş yapmak için **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)** adresine giderek giriş yapabilirsiniz.

---

## **📌 3. Modeli Django Admin Paneline Kaydetme**
Django Admin Paneli’nde **modeli yönetebilmek** için, modeli `myapp/admin.py` dosyasına eklememiz gerekir.

📌 **`myapp/admin.py` dosyasını açın ve aşağıdaki kodu ekleyin:**

```python
from django.contrib import admin
from myapp.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')  # Liste görünümü
    search_fields = ('name',)  # Arama çubuğu ekler
    list_filter = ('created_at',)  # Filtreleme seçenekleri ekler
```

Bu adım tamamlandığında, **admin panelinde `Category` modelini görebileceksiniz.**

---

## **📌 4. Django REST Framework ile API CRUD İşlemleri**
Django REST Framework (DRF) kullanarak **ViewSet** ve **Serializer** yapıları ile API CRUD işlemlerini gerçekleştireceğiz.

### **✅ 1. Serializer Tanımlama**
📌 **`myapp/serializers.py` dosyasını oluşturun ve aşağıdaki kodları ekleyin:**

```python
from rest_framework import serializers
from myapp.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
```
Bu Serializer, **Category modelini JSON formatına çevirmemizi sağlar.**

---

### **✅ 2. ViewSet Tanımlama**
📌 **`myapp/views.py` dosyanızı aşağıdaki şekilde güncelleyin:**

```python
from rest_framework import viewsets
from myapp.models import Category
from myapp.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```
**Ne yaptık?**
- `viewsets.ModelViewSet` kullanarak CRUD işlemleri için **otomatik olarak GET, POST, PUT ve DELETE endpointlerini oluşturduk.**

---

### **✅ 3. URL’leri Tanımlama**
📌 **Ana Django `urls.py` dosyanızı (`djangoapp/urls.py`) açın ve şu satırı ekleyin:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),  # API rotalarını burada dahil ediyoruz
]
```

📌 **`myapp/urls.py` dosyanızı oluşturun ve şu kodları ekleyin:**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API rotalarını otomatik ekliyoruz!
]
```

**Ne yaptık?**
- `DefaultRouter` kullanarak **otomatik olarak CRUD endpointlerini oluşturduk.**
- `/api/categories/` endpointine **GET, POST, PUT ve DELETE istekleri** yapılabilir hale geldi.

---

## **📌 5. Django Sunucusunu Başlatma ve API’yi Test Etme**
Yaptığınız değişiklikleri uygulamak için sunucuyu başlatın:

```sh
python manage.py runserver
```

**📌 API'yi test etmek için aşağıdaki URL'lere istek atabilirsiniz:**

| **İşlem**  | **URL**               | **Metod**  | **Açıklama** |
|------------|----------------------|-----------|-------------|
| **Listele** | `/api/categories/`    | `GET`      | Tüm kategorileri getirir |
| **Ekle**   | `/api/categories/`    | `POST`     | Yeni bir kategori ekler |
| **Detay**  | `/api/categories/1/`  | `GET`      | Belirli bir kategoriyi getirir |
| **Güncelle** | `/api/categories/1/` | `PUT`      | Belirli bir kategoriyi günceller |
| **Sil**    | `/api/categories/1/`  | `DELETE`   | Belirli bir kategoriyi siler |

---

## **📌 Sonuç**
✅ Django REST Framework (DRF) projemize **eklendi ve tanıtıldı**.  
✅ Django Admin Paneli etkinleştirildi ve özelleştirildi.  
✅ Django REST Framework kullanılarak **ViewSet ile CRUD işlemleri** gerçekleştirildi.  
✅ API endpointleri **`/api/categories/`** altında kullanılabilir hale getirildi.  
✅ Sunucu başlatılarak API'nin çalıştığı test edildi.  

🚀 **Şimdi API'yi Postman veya tarayıcıdan test edebilirsin!** 🎯

