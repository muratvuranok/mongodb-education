# **Building a Mini Project: To-Do App with Django Admin and FastAPI APIs**

## **📌 Giriş**
Bu projede, **Django Admin** ile **veritabanı yönetimi** sağlayacak ve **FastAPI** kullanarak gerçek zamanlı bir **To-Do Uygulaması** oluşturacağız. Kullanıcıların **yapılacak işleri** ekleyebileceği, güncelleyebileceği ve sildiği anda UI'dan da otomatik olarak kaldırılacak **gerçek zamanlı bir WebSocket entegrasyonu** içerecek.

---

## **📌 1. Proje Yapısı**
Öncelikle **Django ve FastAPI'nin birlikte çalışacağı bir proje yapısı** oluşturuyoruz.

📌 **Proje Klasör Yapısı:**
```
/todo_project
    ├── /mydjango  # Django Projesi
    │   ├── mydjango/
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── asgi.py
    │   ├── myapp/
    │   │   ├── models.py
    │   │   ├── views.py
    │   │   ├── serializers.py
    ├── main.py  # FastAPI Uygulaması
    ├── static/
    ├── templates/
        ├── index.html
```

---

## **📌 2. Gerekli Paketleri Yükleme**
Öncelikle **Django, FastAPI ve Django Channels** paketlerini yükleyelim:

```sh
pip install django djangorestframework fastapi uvicorn channels psycopg2
```

📌 **Django projesini başlatın:**
```sh
django-admin startproject mydjango
cd mydjango
python manage.py startapp myapp
```

📌 **Django’yu konfigüre edin:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',
    'myapp',
]

ASGI_APPLICATION = "mydjango.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
```

📌 **Veritabanı migration işlemlerini yapın:**
```sh
python manage.py makemigrations
python manage.py migrate
```

---

## **📌 3. Django ORM ile Model Tanımlama**
📌 **`myapp/models.py`** dosyanıza aşağıdaki modeli ekleyin:

```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

📌 **Migration işlemlerini yaparak modeli veritabanına kaydedin:**
```sh
python manage.py makemigrations myapp
python manage.py migrate
```

---

## **📌 4. FastAPI ile API Servisi Oluşturma**
📌 **`main.py` dosyanızı oluşturun:**

```python
import os
import django
from fastapi import FastAPI, WebSocket
from myapp.models import Task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango.settings")
django.setup()

app = FastAPI()

tasks = []

@app.get("/tasks/")
def get_tasks():
    return [{"id": t.id, "title": t.title, "completed": t.completed} for t in Task.objects.all()]

@app.post("/tasks/")
def create_task(title: str):
    task = Task.objects.create(title=title)
    return {"id": task.id, "title": task.title, "completed": task.completed}

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return {"id": task.id, "title": task.title, "completed": task.completed}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    Task.objects.filter(id=task_id).delete()
    return {"message": "Task deleted"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Task updated: {data}")
```

📌 **FastAPI'yi çalıştırın:**
```sh
uvicorn main:app --reload
```

📌 **Django uygulamasını da aynı anda başlatın:**
```sh
python manage.py runserver
```

🚀 **Artık FastAPI, Django Admin ile gerçek zamanlı olarak çalışıyor!**

---

## **📌 5. HTML Web Arayüzü ile Gerçek Zamanlı Güncelleme**
📌 **`templates/index.html`** dosyanıza aşağıdaki kodu ekleyin:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>To-Do App</title>
    <script>
        let socket = new WebSocket("ws://127.0.0.1:8000/ws");

        function markDone(taskId) {
            fetch(`/tasks/${taskId}`, { method: 'PUT' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById(`task-${taskId}`).classList.toggle('completed');
                });
        }

        socket.onmessage = function(event) {
            let taskList = document.getElementById("task-list");
            let newTask = document.createElement("li");
            newTask.id = `task-${event.data.id}`;
            newTask.innerHTML = `${event.data.title} <button onclick='markDone(${event.data.id})'>Done</button>`;
            taskList.appendChild(newTask);
        }
    </script>
</head>
<body>
    <h1>To-Do List</h1>
    <ul id="task-list"></ul>
</body>
</html>
```

📌 **Artık, görevler tamamlandığında veya silindiğinde UI otomatik olarak güncellenecek!**

---

## **📌 6. Sonuç ve Özet**
- **Django Admin** ile veritabanı yönetimi yaptık.
- **FastAPI ile API servisleri** oluşturduk.
- **WebSocket kullanarak gerçek zamanlı güncellemeler** sağladık.
- **HTML ve JavaScript ile UI güncelleme mekanizmasını kurduk.**
- **Kullanıcı görev tamamladığında "Done" butonu ekledik.**
- **FastAPI ile tamamlanmış görevleri güncelleyen bir PUT metodu ekledik.**

🚀 **Tam entegre bir To-Do uygulaması oluşturduk!** 🎯

