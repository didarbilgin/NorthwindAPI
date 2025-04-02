import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np

"""Bu dosya, PostgreSQL veritabanına bağlanmanızı sağlar ve verileri çekmek için gerekli fonksiyonları içerir."""
# load_data update_database check_missing_data


# PostgreSQL bağlantısını oluşturur.
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/GYK2-Northwind"
engine = create_engine(DATABASE_URL)

# Verilen SQL sorgusunu çalıştırır ve sonucu bir DataFrame olarak döndürür.
def fetch_data(query):
    print(f"Sorgu çalıştırılıyor: {query}")
    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)
    df.replace("[null]", np.nan, inplace=True) # '[null]' değerlerini NaN ile değiştirir.
    
    print(f"İlk veri yüklendi:\n{df.head()}\n{'-' * 20}\n")
    return df

# DataFrame'deki eksik değerleri kontrol eder ve ekrana yazdırır.
def check_missing_values(df, table_name):
    print(f"{table_name} tablosundaki eksik veriler kontrol ediliyor...")
    missing = df.isnull().sum()
    print(f"Eksik veriler:\n{missing}\n{'-' * 20}\n")

# DataFrame içindeki sayısal ve metin sütunlarını ayırır ve ekrana yazdırır.
def categorize_columns(df, table_name):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()

    if 'picture' in text_cols:  # 'picture' sütununu metin sütunlarından çıkarır.
        text_cols.remove('picture')
    print(f"{table_name} tablosunda Sayısal Sütunlar: {numeric_cols}")
    print(f"{table_name} tablosunda Metin Sütunlar: {text_cols}\n{'-' * 20}\n")
    return numeric_cols, text_cols



def update_database(engine, data):
    """Veritabanı tablolarını güvenli bir şekilde günceller."""
    update_order = ['categories', 'products', 'customers', 'orders', 'order_details']  
    try:
        with engine.begin() as connection:
            # Foreign key kontrollerini geçici olarak devre dışı bırakır.
            
            connection.execute(text("SET session_replication_role = 'replica'"))
            for table in update_order:
                df = data[table]
                
                # Tabloyu temizler (ancak ID sequence korur).
                connection.execute(text(f"TRUNCATE TABLE {table} CONTINUE IDENTITY CASCADE"))
                
                # Verileri yeniden yükler.
                df.to_sql(table,con=connection,if_exists='append', index=False,chunksize=1000)
                print(f"{table} tablosu başarıyla güncellendi.")
            
            # Foreign key kontrollerini tekrar aktif eder.
            connection.execute(text("SET session_replication_role = 'origin'"))
        
    except Exception as e:
        print(f"Veritabanı güncellemesi başarısız: {e}")
        return False
    return True

