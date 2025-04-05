import pickle
import pandas as pd
import numpy as np

# Kaydedilmiş modeli yükle
def load_model(model_path):
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
    return model_data

# Örnek veri oluştur
def create_sample_data():
    sample_data = {
        'country': ['USA', 'USA','USA'],  # Ülke
        'quantity': [50, 6, 15],                 # Miktar
        'unit_price': [100, 16.8, 16.8],       # Birim fiyat
        'discount': [0.2, 0.05, 0.15],           # İndirim
        'category_id': [7, 5, 2],                # Kategori ID
        'season':['Winter','Summer','Autumn']
    }
    return pd.DataFrame(sample_data)

# Özellik mühendisliği uygula (eğitimdekiyle aynı)
def prepare_sample_data(df):
    df = df.copy()
    df['total_price'] = df['unit_price'] * df['quantity']
    df['discounted'] = (df['discount'] > 0).astype(int)
    return df

# Model ile tahmin yap
def predict_with_model(model_data, sample_df):
    # Özellikleri hazırla
    features = model_data['features']
    sample_df = sample_df[features]
    
    # Kategorik değişkenleri işle
    sample_df = pd.get_dummies(sample_df, columns=['country'])
    
    # Eksik sütunları tamamla (eğitimde olup örnekte olmayan ülkeler)
    missing_cols = set(model_data['model'].feature_names_in_) - set(sample_df.columns)
    for col in missing_cols:
        sample_df[col] = 0
    
    # Sütunları orijinal sıraya göre düzenle
    sample_df = sample_df[model_data['model'].feature_names_in_]
    
    # Tahminleri yap
    predictions = model_data['model'].predict(sample_df)
    predicted_products = model_data['label_encoder'].inverse_transform(predictions)
    
    return predicted_products

# Ana işlem
def main():
    # Modeli yükle
    model_data = load_model("rf_product_model_simple.pkl")
    
    # Örnek veri oluştur
    sample_df = create_sample_data()
    
    # Özellikleri hazırla
    sample_df = prepare_sample_data(sample_df)
    
    # Tahmin yap
    predictions = predict_with_model(model_data, sample_df)
    
    # Sonuçları göster
    print("\nÖrnek Veri:")
    print(sample_df[['country', 'quantity', 'unit_price', 'discount', 'category_id']])
    
    print("\nTahmin Edilen Ürünler:")
    for i, product_id in enumerate(predictions):
        print(f"Örnek {i+1}: {product_id}")

if __name__ == "__main__":
    main()
    