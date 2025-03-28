from sqlalchemy import create_engine, text  # text import edilmeli
# PostgreSQL bağlantı URL'si
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/GYK2-Northwind"  

# Veritabanına bağlan
engine = create_engine(DATABASE_URL)

# Bağlantıyı test et
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM customers"))  
        for row in result:
            print(row)
except Exception as e:
    print(f"Bağlantı hatası: {e}")
