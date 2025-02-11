# Proje Ortam Kurulumu

Bu doküman, projeyi aldıktan sonra gerekli ortam kurulumlarını yapmak için kullanılacak adımları içermektedir.

## 1. Sanal Ortam (Virtual Environment) Oluşturma

Öncelikle yeni bir sanal ortam oluşturun:

```sh
# Windows / Linux / Mac
python -m venv env
```

İsterseniz "env" yerine farklı bir isim verebilirsiniz, örneğin:

```sh
python -m venv elma
```

## 2. Sanal Ortamı Aktif Etme

**Windows için:**

```sh
env\Scripts\activate
```

Eğer özel bir isim verdiyseniz:

```sh
elma\Scripts\activate
```

**Linux / Mac için:**

```sh
source env/bin/activate
```

## 3. Gerekli Paketlerin Yüklenmesi

Aşağıdaki komutları çalıştırarak bağımlılıkları yükleyin:

```sh
pip install pymongo dnspython python-dotenv
```

## 4. `pip` Güncelleme

```sh
python.exe -m pip install --upgrade pip
```

## 5. Bağımlılıkların Yönetimi

Mevcut yüklü paketleri listelemek ve kayıt altına almak:

```sh
pip freeze > requirements.txt
```

Liste halinde kayıtlı olan paketleri yüklemek:

```sh
pip install -r requirements.txt
```

Yeni bir paket yüklediğinizde, bağımlılık listesini güncelleyerek aşağıdaki komutu çalıştırmalısınız:

```sh
pip freeze > requirements.txt
```

## 6. MongoDB Bağlantı Bilgileri

Proje `.env` dosyası içermediğinden, aşağıdaki gibi bir `.env` dosyası oluşturmanız gerekmektedir:

```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=Northwind
```

Bu adımları takip ederek projeyi çalıştırabilirsiniz.
