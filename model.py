import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pickle
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from database import engine

# 1. Veri Yükleme
def load_data():
    query = text("""
SELECT 
    o.order_id,
    o.order_date,
    c.customer_id,
    c.country,
    p.product_id,
    p.product_name,
    p.units_in_stock,
    cat.category_id,
    cat.category_name,
    od.quantity,
    od.discount,
    od.unit_price
FROM orders o
INNER JOIN order_details od ON o.order_id = od.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON od.product_id = p.product_id
INNER JOIN categories cat ON p.category_id = cat.category_id
""")
    return pd.read_sql(query, engine.connect())

df = load_data()



# 2. Özellik Mühendisliği
def prepare_features(df):
    df = df.copy()
    
    # Temel özellikler
    df['total_price'] = df['unit_price'] * df['quantity']
    df['discounted'] = (df['discount'] > 0).astype(int)
    
    return df

df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.month

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df['season'] = df['month'].apply(get_season)
df = prepare_features(df)


# En popüler 10 ürünü seç
top_products = df['product_id'].value_counts().nlargest(10).index
df = df[df['product_id'].isin(top_products)]

# Özellikler ve hedef
features = [
    'country', 'quantity', 'unit_price', 'discount', 
    'total_price', 'discounted','season','category_id'
]

X = df[features]
y = df['product_id']

# Kategorik değişkenleri işle
X = pd.get_dummies(X, columns=['country','season'])

# Label Encoding
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4. Model Kurma
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# Random Forest Modeli
rf_model = RandomForestClassifier(
    n_estimators=100,  # Daha az ağaç
    max_depth=8,       # Daha sığ ağaçlar
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

# 5. Değerlendirme
y_pred = rf_model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_.astype(str)))

# Confusion Matrix
plt.figure(figsize=(12, 10))
disp = ConfusionMatrixDisplay.from_estimator(
    rf_model,
    X_test,
    y_test,
    display_labels=le.classes_,
    xticks_rotation=90,
    cmap=plt.cm.Blues,
    normalize='true'
)
plt.title('Normalized Confusion Matrix')
plt.tight_layout()
plt.show()

# 6. Model Kaydetme
with open("rf_product_model_simple.pkl", "wb") as f:
    pickle.dump({
        'model': rf_model,
        'label_encoder': le,
        'features': features
    }, f)

print("Basit model başarıyla kaydedildi!")