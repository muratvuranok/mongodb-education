pip install fastapi[all] celery redis


celery -A core.celery worker --loglevel=info --pool=solo     # solo windows


pip install flower  # ui

celery -A core.celery flower   