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

from database import fetch_data, check_missing_values, update_database ,engine
"""query = text("SELECT * FROM orders")
df= pd.read_sql(query, engine.connect())
"""
"""
df['order_date'] = pd.to_datetime(df['order_date'])  # Tarih formatına çevir
df['year'] = df['order_date'].dt.year   # Yıl sütunu
df['month'] = df['order_date'].dt.month # Ay sütunu
df['day'] = df['order_date'].dt.day     # Gün sütunu
df['day_of_week'] = df['order_date'].dt.weekday  # Haftanın günü (0 = Pazartesi, 6 = Pazar)
"""
#print(df['year'])


""" 
! postgreSQL sorgusu :
select o.customer_id, sum (od.unit_price*od.quantity) as totalSales from orders o
inner join order_details od on od.order_id=o.order_id
group by o.customer_id
"""

totalSales_query = """
SELECT o.customer_id, 
       SUM(od.unit_price * od.quantity) AS totalSales 
FROM orders o
INNER JOIN order_details od ON od.order_id = o.order_id
GROUP BY o.customer_id;
"""

df_totalsales= pd.read_sql(totalSales_query,engine.connect())
print(df_totalsales)

# Müşterilerin toplam yıllık sipariş tutarını hesapla

# B2B müşteri türüne göre segmentasyon yap
def classify_b2b(sales):
    if sales < 50000:
        return "Small Business"
    elif 50000 <= sales < 200000:
        return "Mid-Sized Business"
    else:
        return "Enterprise"

# !!!!!!segmentasyon degerleri değiştirilebilir!!!!!!
# Segmentasyonu uygula
df_totalsales['classify_b2b'] = df_totalsales['totalsales'].apply(classify_b2b)

# Sonuçları göster
print(df_totalsales.head())


