# pip install fastapi uvicorn

# FastAPI kütüphanesini içe aktarıyoruz ( değişen = değişken )
from fastapi import FastAPI

# FastAPI uygulamasını oluşturuyoruz
app = FastAPI()


# Ana URL ("/") için bir GET isteği endpoint tanımlıyoruz
@app.get("/")
def read_root():
    # Bu endpoint çağrıldığında geriye "Hello, World!" döndürüyoruz
    return {
        "message": "Hello, World!",
        "status": 200,
    }


# HttpGet()
# public async Task<IActionResult> Get(){
#     return Ok("Hello, World!")
# }


# main:app -> main.py dosyasındaki app isimli FastAPI uygulamasını çalıştır
# --reload -> geliştirme sırasında bir değişklik olursa (geliştirme) otomatik olarak yeniden başlatmayı tetikler.

# uvicorn main:app
# dotnet run (program.cs)

# uvicorn main:app --reload
# dotnet watch run (program.cs)





# çalıştırmak için -> uvicorn main:app --reload
