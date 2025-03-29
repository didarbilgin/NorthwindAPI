from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine, text  # text import edilmeli
import pandas as pd
import numpy as np
# PostgreSQL bağlantı URL'si
DATABASE_URL = "postgresql://postgres:Silasila.17@localhost:5432/GYK2Northwind"

# Veritabanına bağlan
engine = create_engine(DATABASE_URL)


# Bağlantıyı test et
"""try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM customers"))  
        for row in result:
            print(row)
except Exception as e:
    print(f"Bağlantı hatası: {e}")
"""
""" Fonksiyonel Gereksinimler Northwind veritabanından veri çekilecek.

Gerekli veri ön işleme adımları yapılacak.-

Ürün bazlı geçmiş satış verilerine göre tahmin modeli oluşturulacak.."""

"""Orders

Order_Details

Products

Customers

Categories (opsiyonel)"""

try:
    with engine.connect() as connection:
        query = text("SELECT * FROM orders")
        df_orders = pd.read_sql(query, connection)

        query = text("SELECT * FROM customers")
        df_customers = pd.read_sql(query, connection)

        query = text("SELECT * FROM order_details")
        df_order_details=pd.read_sql(query, connection)

        query = text("SELECT * FROM products")
        df_products=pd.read_sql(query, connection)


        query = text("SELECT * FROM categories")
        df_categories=pd.read_sql(query, connection)


        print(df_customers.head())
        print("*****************")
        print(df_products.head())
        print("*****************")
        print(df_categories.head())
        print("*****************")
        print(df_order_details.head())
        
except Exception as e:
    print(f"Bağlantı hatası: {e}")

# Eksik veri kontrolü
print("Eksik veri kontrolü:")
for df, name in zip([df_orders, df_categories, df_customers, df_products, df_order_details],
                    ["orders", "categories", "customers", "products", "order_details"]):
    print(f"{name}:")
    print(df.isnull().sum())
    print("*****")

# Eksik ship_region verilerini en sık görülen değerle doldur
if 'ship_region' in df_orders.columns:
    df_orders['ship_region'].replace(to_replace=[None], value=np.nan, inplace=True)
    imputer = SimpleImputer(strategy='most_frequent')
    df_orders[['ship_region']] = imputer.fit_transform(df_orders[['ship_region']])

# Orders tablosundaki verileri güvenli bir şekilde güncelleme
from sqlalchemy.exc import IntegrityError

try:
    with engine.begin() as connection:  # begin() otomatik transaction yönetimi sağlar
        # 1. Önce foreign key constraint'i geçici olarak devre dışı bırak
        connection.execute(text("ALTER TABLE order_details DROP CONSTRAINT IF EXISTS fk_order_details_orders"))
        
        # 2. Orders tablosunu truncate et (DELETE yerine daha verimli)
        connection.execute(text("TRUNCATE TABLE orders RESTART IDENTITY CASCADE"))
        
        # 3. Yeni verileri ekle
        df_orders.to_sql('orders', con=connection, if_exists='append', index=False)
        
        # 4. Foreign key constraint'i yeniden oluştur
        connection.execute(text("""
            ALTER TABLE order_details 
            ADD CONSTRAINT fk_order_details_orders 
            FOREIGN KEY (order_id) REFERENCES orders(order_id) 
            ON DELETE CASCADE
        """))
        print("\nOrders tablosu veritabanına başarıyla kaydedildi!")
        
except IntegrityError as e:
    print(f"Referans bütünlüğü hatası: {e}")
    # Rollback otomatik olarak yapılacak
except Exception as e:
    print(f"Diğer veri güncelleme hatası: {e}")