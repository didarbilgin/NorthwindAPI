import pandas as pd
import pickle
import numpy as np

# Model ve label encoder yükleniyor
with open("ensemble_model.pkl", "rb") as model_file:
    loaded_model = pickle.load(model_file)

with open("label_encoder.pkl", "rb") as le_file:
    loaded_le = pickle.load(le_file)

# Örnek veri (tek satır)
"""sample_data = {
    "month": 7,
    "country": "USA",
    "discount": 0.2,
    "unit_price": 17,
    "units_in_stock": 40,
    "season": "Summer",
    "total_sales": 2462.4
}"""
sample_data = {
    "country": "Venezuela",
    "season": "Spring",
    "quantity": 50
}

# DataFrame'e çevir (tek satır için köşeli parantez önemli!)
df_test = pd.DataFrame([sample_data])

# One-hot encoding
df_encoded = pd.get_dummies(df_test)

# Eğitim verisinde bulunan tüm kolonları kontrol et
expected_features = loaded_model.feature_names_in_

# Eksik kolonları tamamla (sıfır değerler ile)
for col in expected_features:
    if col not in df_encoded.columns:
        df_encoded[col] = 0

# Kolon sırasını eşleştir (eğitimdeki sıralama ile aynı olmalı)
df_encoded = df_encoded[expected_features]

# Tahmin yap
predicted_value = loaded_model.predict(df_encoded)

# Tahmin edilen product_id'yi geri çevirmek için label encoder'ı kullanıyoruz
predicted_product_id = loaded_le.inverse_transform(predicted_value)

print(f"Tahmin edilen product_id: {predicted_product_id[0]}")