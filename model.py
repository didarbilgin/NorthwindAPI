import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from database import engine
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score 
from sqlalchemy import create_engine, text
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.metrics import mean_squared_error, r2_score
from database import fetch_data, check_missing_values, update_database ,engine
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
import pickle


query = text("""SELECT o.order_id,c.customer_id, o.order_date ,c.country, p.product_id, p.product_name , od.quantity, od.discount, od.unit_price, p.units_in_stock  FROM orders o 
inner join order_details od 
on o.order_id = od.order_id 
inner join customers c
on o.customer_id = c.customer_id
inner join products p 
on od.product_id = p.product_id """)
df= pd.read_sql(query, engine.connect())


df['order_date'] = pd.to_datetime(df['order_date'])  # Tarih formatına çevir
df['month'] = df['order_date'].dt.month # Ay sütunu

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df["season"] = df["month"].apply(get_season)

def prepare_data(df):
    df = df.copy()
    # Yeni özellik oluştur: Total Sales
    df["total_sales"] = df["unit_price"] * df["quantity"] * (1 - df["discount"])

    # Gerekli sütunları seç
    X = df[["month", "country","discount", "unit_price", "units_in_stock", "season","total_sales"]]
    y = df["product_id"]

    return X, y

X, y = prepare_data(df)
X_encoded = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

xgb_model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)


rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

def evaluate_model(y_test, y_pred, model_name):
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"{model_name} Performansı:")
    print(f"MSE: {mse:.4f}")
    print(f"R²: {r2:.4f}\n{'-'*30}")

evaluate_model(y_test, y_pred_xgb, "XGBoost")
evaluate_model(y_test, y_pred_rf, "Random Forest")
evaluate_model(y_test, y_pred_gb, "Gradient Boosting")

y_pred_ensemble = (y_pred_xgb  + y_pred_rf + y_pred_gb) / 3
evaluate_model(y_test, y_pred_ensemble, "Ensemble (XGBoost + RF + GB)")

estimators = [
    ('xgb', xgb_model),
    ('rf', rf_model),
    ('gb', gb_model)
    ]
stacking_model = StackingRegressor(estimators=estimators, final_estimator=RandomForestRegressor(n_estimators=100, random_state=42))
stacking_model.fit(X_train, y_train)
y_pred_stacking = stacking_model.predict(X_test)
evaluate_model(y_test, y_pred_stacking, "Stacking Model")


with open("stacking_model.pkl", "wb") as model_file:
        pickle.dump(stacking_model, model_file)

with open("scaler.pkl", "wb") as scaler_file:
        pickle.dump(scaler, scaler_file)

