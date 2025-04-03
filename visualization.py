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


top_products = df.groupby("product_name")["quantity"].sum().nlargest(10).index
filtered_df = df[df["product_name"].isin(top_products)]



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
