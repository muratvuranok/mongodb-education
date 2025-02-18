env file oluşturma  python -m venv env

env\script\active

pip install django

 
proje oluşturma işlemi


django-admin startproject <proje adi>
django-admin startproject myapp


projeyi çalıştırma 

manage.py dizininde olduğunuzdan emin olun, sonrasında

python manage.py runserver



migration işlemleri


python manage.py migrate  -- var olan migration'ları execute etme işlemi 
python manage.py runserver




panel için süper kullanıcı oluşturduk :)
python manage.py createsuperuser


python manage.py startapp categoryapp

python manage.py makemigrations  -> migration ekleme
python manage.py migrate  -- var olan migration'ları execute etme işlemi 


<!-- 
prje içerisine indiricez

pip install djangorestframework 

-->
