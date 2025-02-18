# **Real-Time Applications Using Django Channels**

## **📌 Giriş**
Geleneksel Django uygulamaları **senkron** olarak çalışırken, **gerçek zamanlı** uygulamalar oluşturmak için **asenkron** desteğe ihtiyaç duyarız. **Django Channels**, WebSocket desteği, arka plan görevleri ve asenkron işlemleri Django'ya ekleyerek bu ihtiyacı karşılar.

Bu rehberde, **Django Channels kullanarak gerçek zamanlı bir sohbet uygulaması geliştireceğiz.**

---

## **📌 1. Django Channels Kurulumu ve Konfigürasyonu**
Öncelikle **Django Channels** paketini yükleyelim:

```sh
pip install channels
```

📌 **`settings.py` içinde gerekli ayarları ekleyin:**

```python
INSTALLED_APPS = [
    'daphne',  # Django Channels için gerekli
    'channels',
    'myapp',
]

ASGI_APPLICATION = "mydjango.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # Test amaçlı bellek içi backend
    },
}
```

📌 **ASGI yapılandırmasını ekleyin (`mydjango/asgi.py`):**

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
```

---

## **📌 2. WebSocket Endpoint Oluşturma**
**Django Channels**, WebSocket bağlantılarını yönetmek için özel bir **consumer** kullanır.

📌 **`myapp/consumers.py` dosyasını oluşturun:**

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Bağlantı başarılı!"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        await self.send(text_data=json.dumps({"message": message}))
```

📌 **WebSocket URL'lerini tanımlayın (`myapp/routing.py`):**

```python
from django.urls import re_path
from myapp.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
]
```

---

## **📌 3. Django Channels ile WebSocket Bağlantısı**
Artık **WebSocket bağlantısını test edebiliriz!**

📌 **Django ve ASGI sunucusunu çalıştırın:**

```sh
python manage.py runserver
```

📌 **WebSocket bağlantısını test etmek için:**
1. **Tarayıcı konsolunu açın** (F12 > Console).
2. Aşağıdaki kodu yazın:

```javascript
let socket = new WebSocket("ws://127.0.0.1:8000/ws/chat/");

socket.onopen = function(event) {
    console.log("WebSocket bağlantısı açıldı.");
    socket.send(JSON.stringify({"message": "Merhaba, dünya!"}));
};

socket.onmessage = function(event) {
    console.log("Mesaj alındı:", event.data);
};
```

📌 **Çıkış Beklentisi:**
```json
{"message": "Bağlantı başarılı!"}
{"message": "Merhaba, dünya!"}
```

---

## **📌 4. Redis ile Gerçek Zamanlı Kanal Katmanı (Opsiyonel)**
Gerçek dünya uygulamalarında **InMemoryChannelLayer yerine Redis** kullanmalıyız.

📌 **Redis ve ilgili paketi yükleyin:**

```sh
pip install channels-redis
```

📌 **`settings.py` içinde Redis kanal katmanını ayarlayın:**

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

📌 **Redis’i başlatın:**

```sh
redis-server
```

📌 **Django uygulamasını tekrar başlatın:**

```sh
python manage.py runserver
```

---

## **📌 5. Gerçek Zamanlı Sohbet Uygulaması (Gelişmiş Kullanım)**
Daha karmaşık **grup bazlı sohbet odaları** oluşturmak için `Channel Layers` kullanabiliriz.

📌 **Gelişmiş `ChatConsumer` sınıfı:**

```python
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "general"
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
```

Bu yapı sayesinde tüm bağlı istemciler, gelen mesajları **gerçek zamanlı olarak** alır! 🚀

---

## **📌 6. Özet ve Sonuç**
- Django Channels ile **WebSocket desteği** ekledik.
- **Gerçek zamanlı mesaj iletimi** sağladık.
- **Redis ile performansı artırdık**.
- **Grup bazlı chat sistemi** geliştirdik.

🚀 **Artık Django ile gerçek zamanlı uygulamalar geliştirebilirsiniz!** 🎯

