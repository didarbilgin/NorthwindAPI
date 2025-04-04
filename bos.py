from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier, VotingClassifier
import xgboost as xgb
import pickle
from sqlalchemy import text
from database import engine

# Veritabanından veriyi al
query = text("""
SELECT o.order_id, c.customer_id, o.order_date, c.country, p.product_id, 
       p.product_name, od.quantity, od.discount, od.unit_price, p.units_in_stock
FROM orders o 
INNER JOIN order_details od ON o.order_id = od.order_id 
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON od.product_id = p.product_id
""")
df = pd.read_sql(query, engine.connect())

# Tarih formatı ve mevsim bilgisi
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

# Veri Hazırlama Fonksiyonu
def prepare_data(df):
    df = df.copy()
    df["total_sales"] = df["unit_price"] * df["quantity"] * (1 - df["discount"])
    return df

# Top 10 ürünleri filtrele
top_products = df['product_id'].value_counts().nlargest(10).index
df = df[df['product_id'].isin(top_products)]

# Veriyi hazırlama
df = prepare_data(df)

# Özellikleri ve hedefi ayır
#X = df[["month", "country", "discount", "unit_price", "units_in_stock", "season", "total_sales"]]
X = df[[ "country",  "season", "quantity"]]
y = df["product_id"]

# Kategorik özellikleri sayısal hale getirme
X_encoded = pd.get_dummies(X)

# Etiketleri sayısal hale getirme
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# Modelleri tanımla
xgb_clf = xgb.XGBClassifier(eval_metric="mlogloss", use_label_encoder=False, random_state=42)
rf_clf = RandomForestClassifier(random_state=42)
gb_clf = GradientBoostingClassifier(random_state=42)

# Ensemble model (Voting Classifier)
ensemble_clf = VotingClassifier(
    estimators=[('xgb', xgb_clf), ('rf', rf_clf), ('gb', gb_clf)],
    voting='soft'
)

# Modeli eğit
ensemble_clf.fit(X_train, y_train)

# Test seti üzerinde tahmin yap
y_pred = ensemble_clf.predict(X_test)

# Başarı ölçümleri
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=le.classes_.astype(str), zero_division=0)
cm = confusion_matrix(y_test, y_pred)

# Confusion Matrix görselleştirmesi
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
disp.plot(xticks_rotation=90)
plt.title(f'Confusion Matrix (Accuracy: {acc:.2f})')
plt.tight_layout()
plt.show()

# Sonuçlar
print(f"Doğruluk (Accuracy): {acc:.4f}\n")
print("Sınıflandırma Raporu:\n")
print(report)

# Modelleri Kaydet
# Ensemble modelini kaydet
with open("ensemble_model.pkl", "wb") as model_file:
    pickle.dump(ensemble_clf, model_file)

# LabelEncoder'ı kaydet
with open("label_encoder.pkl", "wb") as le_file:
    pickle.dump(le, le_file)

print("Modeller başarıyla kaydedildi!")

# Kaydedilen modeli yükleme (test için)
with open("ensemble_model.pkl", "rb") as model_file:
    loaded_model = pickle.load(model_file)

with open("label_encoder.pkl", "rb") as le_file:
    loaded_le = pickle.load(le_file)

# Test: Yüklenen model ile tahmin yapma
y_pred_loaded_model = loaded_model.predict(X_test)
print(f"Yüklenen modelin doğruluğu: {accuracy_score(y_test, y_pred_loaded_model):.4f}")
