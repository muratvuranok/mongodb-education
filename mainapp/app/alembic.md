`pip install alembic`

`alembic init alembic`


alembic.ini -> `sqlalchemy.url = sqlite:///./test.db`  olarak düzenleyin


alembic folder içerisinde yer alan env.py içerine
`from core.database import` Base ekleyin 
`target_metadata = Base.metadata` burdaki gibi düzenleyin



migrartion ekleme
`alembic revision --autogenerate -m "Initial migration"`


migration çalıştırma
`alembic upgrade head`