import pickle
import pandas as pd
import numpy as np

# Load the saved model
def load_model(model_path):
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
    return model_data

# Create sample data
def create_sample_data():
    sample_data = {
        'country': ['USA', 'Switzerland', 'France'],  # Country
        'quantity': [50, 6, 15],           # Quantity
        'unit_price': [100, 16.8, 16.8],   # Unit price
        'discount': [0.2, 0.05, 0.15],     # Discount
        'category_id': [7, 5, 2],          # Category ID
        'season': ['Winter', 'Summer', 'Autumn']  # Season
    }
    return pd.DataFrame(sample_data)

# Apply feature engineering (same as during training)
def prepare_sample_data(df):
    df = df.copy()
    df['total_price'] = df['unit_price'] * df['quantity']
    df['discounted'] = (df['discount'] > 0).astype(int)
    return df

# Make predictions with the model
def predict_with_model(model_data, sample_df):
    # Prepare features
    features = model_data['features']
    sample_df = sample_df[features]
    
    # Handle categorical variables
    sample_df = pd.get_dummies(sample_df, columns=['country'])
    
    # Fill missing columns (for countries not present in the example but in the training)
    missing_cols = set(model_data['model'].feature_names_in_) - set(sample_df.columns)
    for col in missing_cols:
        sample_df[col] = 0
    
    # Reorder columns according to the original feature order
    sample_df = sample_df[model_data['model'].feature_names_in_]
    
    # Make predictions
    predictions = model_data['model'].predict(sample_df)
    predicted_products = model_data['label_encoder'].inverse_transform(predictions)
    
    return predicted_products

# Main process
def main():
    # Load the model
    model_data = load_model("rf_product_model.pkl")
    
    # Create sample data
    sample_df = create_sample_data()
    
    # Prepare features
    sample_df = prepare_sample_data(sample_df)
    
    # Make predictions
    predictions = predict_with_model(model_data, sample_df)
    
    # Display the results
    print("\nSample Data:")
    print(sample_df[['country', 'quantity', 'unit_price', 'discount', 'category_id']])
    
    print("\nPredicted Products:")
    for i, product_id in enumerate(predictions):
        print(f"Sample {i+1}: {product_id}")

if __name__ == "__main__":
    main()
