# Celery ile Asenkron Görev Yönetimi - FastAPI Entegrasyonu

Bu dökümanda **Celery**'yi **FastAPI** ile entegre ederek asenkron görevler oluşturmayı, çalıştırmayı ve yönetmeyi adım adım anlatacağız. 
Ayrıca **tekrarlı (periyodik) görevler**, **Web UI kurulumu (Flower UI)** ve **çakışmaları önleme mekanizmaları** gibi ek konuları da ele alacağız.

---

## 🚀 1. Gerekli Bağımlılıkları Yükleme

Celery'yi FastAPI ile kullanabilmek için aşağıdaki paketleri yüklememiz gerekiyor.

```bash
pip install fastapi[all] celery redis pydantic celery[redis] celery-beat flower
```

### **Bağımlılık Açıklamaları**
| Paket | Açıklama |
|--------|----------|
| `fastapi` | Web framework |
| `celery` | Asenkron görev yönetimi |
| `redis` | Celery için broker ve backend |
| `pydantic` | Veri doğrulama için |
| `celery-beat` | Periyodik görevler için |
| `flower` | Web UI ile görev yönetimi |


---

## 🎯 2. Redis Sunucusunu Başlatma

Redis, Celery'nin **broker** ve **backend** olarak kullanacağı bir mesaj kuyruğu sistemidir.

**Docker Kullanarak Redis Çalıştırma:**
```bash
docker run -d --name redis -p 6379:6379 redis
```

Eğer Docker yoksa, Redis'i sisteminize kurmanız gerekmektedir.


---

## 🏗️ 3. Proje Yapısı

Dosya yapımız aşağıdaki gibidir:
```
mainapp/
│── core/
│   │── config.py
│   │── celery.py  # Celery uygulaması
│
│── tasks/
│   │── email_tasks.py  # Görevlerin tanımlandığı yer
│
│── api/
│   │── task.py  # FastAPI endpointleri
│
│── schemas/
│   │── email.py  # Veri doğrulama için Pydantic modeli
│
│── main.py  # FastAPI uygulaması
```

---

## ⚙️ 4. Celery Yapılandırması (`core/celery.py`)

Celery uygulamamızı `core/celery.py` dosyasında tanımlıyoruz:

```python
from celery import Celery
from core.config import settings

REDIS_URL = settings.REDIS_URL

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.email_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
```

🔹 **Broker**: Görevlerin kuyruklandığı yerdir. Biz **Redis** kullanıyoruz.  
🔹 **Backend**: Görev sonuçlarını saklar.  
🔹 **Task Serializer**: Görevlerin JSON formatında serileştirilmesini sağlar.

---

## 📊 7. Flower UI ile Görev Yönetimi

Celery için bir **Web UI** kullanmak isterseniz **Flower** kurabilirsiniz.

### **Flower Paketini Yükleme:**
```bash
pip install flower
```

### **Flower'ı Çalıştırma:**
```bash
celery -A core.celery.celery_app flower
```

🌍 **Varsayılan URL:** `http://localhost:5555`

### **Flower ile Yapabileceklerin:**
- Çalışan görevleri izleyebilirsin.
- Task kuyruklarını yönetebilirsin.
- Worker'ları görüntüleyebilir ve kontrol edebilirsin.
- Görev istatistiklerini inceleyebilirsin.

🚀 **Flower, Celery görevlerini takip etmek için güçlü bir Web UI sağlar.**

---

## 🔁 8. Tekrarlı Görevlerde Çakışmayı Önleme Senaryosu

**Çözüm Kodu:**
```python
@celery_app.task(name="tasks.email_tasks.periodic_task")
def periodic_task():
    task_key = "tasks.email_tasks.periodic_task"
    
    if redis_client.get(task_key):
        print("Task already running, skipping new execution.")
        return "Previous task still running, skipping this execution."
    
    redis_client.set(task_key, "running", ex=360)  # 6 dakika süresi
    
    print("Bu görev her 5 dakikada bir çalışır!")
    time.sleep(300)
    print("Görev tamamlandı!")
    redis_client.delete(task_key)
    return "Task Completed"
```

🚀 **Böylece aynı anda birden fazla görev çalışmasını engellemiş olduk.**

