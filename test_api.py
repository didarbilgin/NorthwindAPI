from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model on startup
model_data = pickle.load(open("rf_product_model_simple.pkl", "rb"))

def prepare_sample_data(df):
    df = df.copy()
    df['total_price'] = df['unit_price'] * df['quantity']
    df['discounted'] = (df['discount'] > 0).astype(int)
    return df

def predict_with_model(model_data, sample_df):
    features = model_data['features']
    sample_df = sample_df[features]

    sample_df = pd.get_dummies(sample_df, columns=['country'])

    missing_cols = set(model_data['model'].feature_names_in_) - set(sample_df.columns)
    for col in missing_cols:
        sample_df[col] = 0

    sample_df = sample_df[model_data['model'].feature_names_in_]
    predictions = model_data['model'].predict(sample_df)
    predicted_products = model_data['label_encoder'].inverse_transform(predictions)

    # 👇 NumPy array'i saf Python listesine dönüştür
    return predicted_products.tolist()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data)
    df = prepare_sample_data(df)
    predictions = predict_with_model(model_data, df)
    return jsonify({'predictions': predictions})

if __name__ == '__main__':
    app.run(debug=True)
