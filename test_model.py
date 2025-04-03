import pandas as pd
import pickle
import numpy as np

# Model ve scaler yükleniyor
with open("stacking_model.pkl", "rb") as model_file:
    loaded_model = pickle.load(model_file)

with open("scaler.pkl", "rb") as scaler_file:
    loaded_scaler = pickle.load(scaler_file)

# Örnek veri (tek satır)
sample_data = {
    "month": 7,
    "country": "Brazil",
    "discount": 0.15,
    "unit_price": 16.8,
    "units_in_stock": 76,
    "season": "Summer",
    "total_sales": 214.2
}

# DataFrame'e çevir (tek satır için köşeli parantez önemli!)
df_test = pd.DataFrame([sample_data])

# One-hot encoding
df_encoded = pd.get_dummies(df_test)

# Eksik kalan kolonları (eğitim sırasında var olan ama burada olmayanları) tamamla
expected_features = loaded_scaler.feature_names_in_
for col in expected_features:
    if col not in df_encoded.columns:
        df_encoded[col] = 0

# Kolon sırasını eşleştir
df_encoded = df_encoded[expected_features]

# Ölçekleme
df_scaled = loaded_scaler.transform(df_encoded)

# Tahmin
predicted_value = loaded_model.predict(df_scaled)
print(f"Tahmin edilen product_id: {predicted_value[0]:.2f}")