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

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score 
from sqlalchemy import create_engine, text

from database import load_data, check_missing_data, update_database ,engine

#ürün bazlı satış miktarı 

#ay bazlı satış miktarı

query = text("SELECT * FROM orders")
df= pd.read_sql(query, engine.connect())


df['order_date'] = pd.to_datetime(df['order_date'])  # Tarih formatına çevir
df['year'] = df['order_date'].dt.year   # Yıl sütunu
df['month'] = df['order_date'].dt.month # Ay sütunu
df['day'] = df['order_date'].dt.day     # Gün sütunu
df['day_of_week'] = df['order_date'].dt.weekday  # Haftanın günü (0 = Pazartesi, 6 = Pazar)

print(df['year'])