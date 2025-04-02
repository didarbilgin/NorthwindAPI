"""Makine öğrenmesi modeli burada eğitilecek ve kaydedilecektir."""
"""  Makine Öğrenmesi Modeli
        1.	Hedef değişken belirlenecek (örneğin: ürün bazlı satış miktarı).
        2.	Eğitim ve test verisinin hazırlanması (train_test_split).
        3.	Model seçimi yapılacak.
        4.	Modelin eğitilmesi ve test edilmesi.
        5.	Model başarım metriklerinin raporlanması (R2, RMSE, vb.).
        6.	Eğitilmiş modelin .pkl veya benzeri formatta kaydedilmesi.
"""
"""yapılacaklar :
    1.veriyi yükleme 
    2.hedef değişkenleri belirleme : bağımlı ve bağımsız değişkenler
    3.veri setini train ve test değerlerine ayırma 
    4.model seç ve eğit 
    5.model performansını değerlendirme
      """
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from database import engine

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score 
from sqlalchemy import create_engine, text
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from database import fetch_data, check_missing_values, update_database ,engine


query = text("""SELECT o.order_id,c.customer_id, o.order_date ,c.country, p.product_id, p.product_name , od.quantity, od.discount, od.unit_price, p.units_in_stock  FROM orders o 
inner join order_details od 
on o.order_id = od.order_id 
inner join customers c
on o.customer_id = c.customer_id
inner join products p 
on od.product_id = p.product_id """)
df= pd.read_sql(query, engine.connect())


df['order_date'] = pd.to_datetime(df['order_date'])  # Tarih formatına çevir
#df['year'] = df['order_date'].dt.year   # Yıl sütunu
df['month'] = df['order_date'].dt.month # Ay sütunu
#df['day'] = df['order_date'].dt.day     # Gün sütunu
#df['day_of_week'] = df['order_date'].dt.weekday  # Haftanın günü (0 = Pazartesi, 6 = Pazar)


#print(df['year'])



# Müşterilerin toplam yıllık sipariş tutarını hesapla

# Sonuçları göster
