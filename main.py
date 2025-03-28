from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine, text  # text import edilmeli
import pandas as pd
import numpy as np
# PostgreSQL bağlantı URL'si
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/GYK2-Northwind"  

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

#null veri kontrol etme işlemi 
print(df_order_details.isnull().sum())
print("*****")
print(df_categories.isnull().sum())
print("*****")
print(df_customers.isnull().sum())
print("*****")
print(df_products.isnull().sum())
print("*****")
print(df_orders.isnull().sum())


#STRING DEGERLERİ DOLDURMA İŞLEMİ "EN ÇOK" VERİYE GÖRE

df_orders['ship_region'].replace(to_replace=[None], value=np.nan, inplace=True)
imputer = SimpleImputer(strategy='most_frequent')
df_orders[['ship_region']] = imputer.fit_transform(df_orders[['ship_region']])
print(df_orders)
# Yeni verileri mevcut tabloya eklemek için 'append' kullanabilirsiniz
#df_cleaned = pd.DataFrame(df_orders, columns=df_orders.columns)
df_orders.to_sql('orders', con=engine, if_exists='replace', index=False)

print("\nOrders tablosu veritabanına başarıyla kaydedildi!")