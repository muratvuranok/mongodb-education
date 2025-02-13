from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.confg import settings


# **Sqlite bağlantısı oluşturma**
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})


# `connect_args={"check_same_thread": False}` -> sqlite bağlantısını thread-safe yapar. Sqlite, thread-safe değildir. Bu yüzden bu parametre kullanılır. Diğer veritabanları için bu parametre kullanılmaz. Sqlite'ın tek thread (iş parçacığı) sınırlandırmasını kaldırmak için kullanılır.


# **Session yönetimi**
SessionLocal = sessionmaker(
    autocommit=False,  # Otomatik commit işlemi yapma (False) -> Manuel commit işlemi yapılacak, işlem başarılı olursa commit edilecek, True olursa otomatik commit yapılacak.
    autoflush=False,
    bind=engine,
)


# **ORM Base sınıfı oluşturma**
Base = declarative_base()

#  **Modellerin `Base` içine eklenmesi**
import models.category

# import models.product
# import models.user
# import models.order

# **Veri tabanı tablolarını oluştur**
Base.metadata.create_all(bind=engine)


# **Veritabanı bağlantısını sağlayan bağımlılık**
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
