import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

"""Bu dosya, PostgreSQL veritabanına bağlanmanızı sağlar ve verileri çekmek için gerekli fonksiyonları içerir."""


# Database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/GYK2-Northwind"
engine = create_engine(DATABASE_URL)

def load_data(engine):
    """Load all tables from database"""
    tables = ['categories', 'customers', 'order_details', 'orders', 'products']
    data = {}
    
    try:
        with engine.connect() as connection:
            for table in tables:
                data[table] = pd.read_sql_table(table, connection)
        print("Data loaded successfully")
        return data
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None

def update_database(engine, data):
    """Update database tables safely"""
    # Define update order based on foreign key dependencies
    update_order = ['categories', 'products', 'customers', 'orders', 'order_details']
    
    try:
        with engine.begin() as connection:
            # Disable triggers temporarily to avoid constraint issues
            connection.execute(text("SET session_replication_role = 'replica'")) 
            #replica olarak ayarlamak, veriyi güncellerken hata almamak için tetikleyicileri kapatır.
            
            for table in update_order:
                # Get the DataFrame
                df = data[table]
                
                # Clear existing data
                connection.execute(text(f"TRUNCATE TABLE {table} CONTINUE IDENTITY CASCADE"))
                
                # Insert new data
                df.to_sql(table,con=connection,if_exists='append',index=False,chunksize=1000)
                print(f"{table} table updated successfully")
            
            #Tetikleyicileri ve yabancı anahtar kısıtlamalarını tekrar açıyor.
            connection.execute(text("SET session_replication_role = 'origin'")) 
            

            
    except SQLAlchemyError as e:
        print(f"Database update failed: {e}")
        return False
    return True

def check_missing_data(data):
    """Check for missing values in all DataFrames"""
    print("\nMissing data check:")
    for name, df in data.items():
        print(f"{name}:")
        print(df.isnull().sum())
        print("*****")

"""TRUNCATE TABLE {table} → İlgili tablodaki tüm verileri siler.
                CONTINUE IDENTITY CASCADE:
                    CONTINUE IDENTITY → Otomatik artan (AUTO_INCREMENT veya SERIAL) ID değerlerini sıfırlamaz.
                    CASCADE → Eğer tablo başka tablolara bağlıysa, bağlı olan verileri de siler."""
                