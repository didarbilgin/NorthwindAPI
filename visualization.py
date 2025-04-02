from database import fetch_data, check_missing_values, update_database ,engine
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from database import engine
from model import df
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report 
from sqlalchemy import create_engine, text
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier

def get_season(month):
    if month in [12, 1, 2]:
        return 'Kış'
    elif month in [3, 4, 5]:
        return 'İlkbahar'
    elif month in [6, 7, 8]:
        return 'Yaz'
    else:
        return 'Sonbahar'

top_products = df.groupby("product_name")["quantity"].sum().nlargest(10).index
filtered_df = df[df["product_name"].isin(top_products)]

df["season"] = df["month"].apply(get_season)



fig = px.choropleth(df,
    locations="country",
    locationmode="country names",
    color="quantity",
    color_continuous_scale="Reds", # renk skalası
    title="Ülke Bazlı Isı Haritası")

#fig.show()

#print(df)

# hangi ürünün hangi mevsimde satıldığını gösteren bir model
def correlation_heatmap(df, table_name):
    """
    Sayısal sütunlar arasındaki korelasyonları ısı haritası ile gösterir.
    """
    plt.figure(figsize=(10, 6))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title(f"{table_name} Tablosu Korelasyon Matrisi")
    plt.show()

#correlation_heatmap(df, "Ürünler")

plt.figure(figsize=(10,6))
sns.barplot(x='season', y='quantity', data=df)
plt.title("Mevsimlere Göre Toplam Satış Miktarı")
plt.ylabel("Satış Miktarı")
plt.xlabel("Mevsim")
plt.show()

#model eğitiminde sayısal veriler kullanılacak
# Ülke + mevsim + ürün bazlı toplam satış
X = df[["month", "country"]]
y = df["product_id"]

# Kategorik değişkenleri encode et
X_encoded = pd.get_dummies(X)

valid_products = y.value_counts()[y.value_counts() > 1].index
X_filtered = X_encoded[y.isin(valid_products)]
y_filtered = y[y.isin(valid_products)]

# Train/Test ayır
X_train, X_test, y_train, y_test = train_test_split(
    X_filtered, y_filtered, test_size=0.2, random_state=42, stratify=y_filtered
)

# Modeli eğit
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Tahmin ve başarı
y_pred = model.predict(X_test)
print("Doğruluk (Accuracy):", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Yeni veri: örneğin Almanya'da kış ayında ne satılır?
sample = pd.DataFrame({
    "month": [1],
    "country": ["Germany"]
})
sample_encoded = pd.get_dummies(sample)

# Eksik sütunları doldur (train sütunlarına göre hizalama)
for col in X_encoded.columns:
    if col not in sample_encoded:
        sample_encoded[col] = 0

# Sıralamayı eşleştir
sample_encoded = sample_encoded[X_encoded.columns]

# Tahmin et
predicted_product_id = model.predict(sample_encoded)[0]
print("Tahmin edilen ürün ID:", predicted_product_id)

