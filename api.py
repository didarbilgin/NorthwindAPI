"""FastAPI will be used to create API endpoints. 
This file provides functionality such as listing products, making predictions, and training the model."""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import pickle
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager

# --- Database and Application Configuration ---
# PostgreSQL database connection string
DATABASE_URL = "postgresql://postgres:271003@localhost:5432/gyk2northwind"

# SQLAlchemy engine and session configuration
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy Models ---
class ProductDB(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    unit_price = Column(Float)
    units_in_stock = Column(Integer)
    category_id = Column(Integer)

# --- Pydantic Models ---
class Product(BaseModel):
    product_id: int
    product_name: str
    unit_price: float
    units_in_stock: int
    category_id: int
    
    class Config:
        from_attributes = True

class ProductItem(BaseModel):
    unit_price: float
    quantity: int
    discount: float
    country: str
    season: str
    category_id: int

class ProductItems(BaseModel):
    items: List[ProductItem]

# --- Application Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown operations for the application"""
    # Test the database connection on startup
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✓ PostgreSQL connection successful")
    except Exception as e:
        print(f"✗ PostgreSQL connection error: {e}")
    
    # Create tables (only in development)
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown operations (optional)
    print("Shutting down application...")

app = FastAPI(lifespan=lifespan)

# --- Helper Functions ---
def get_db():
    """Provides a new database session for each request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def prepare_sample_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepares incoming data for the model"""
    df = df.copy()
    df['total_price'] = df['unit_price'] * df['quantity']
    df['discounted'] = (df['discount'] > 0).astype(int)
    return df

# --- Machine Learning Model ---
try:
    model_data = pickle.load(open("rf_product_model.pkl", "rb"))
except Exception as e:
    raise RuntimeError(f"Model could not be loaded: {str(e)}")

def predict_with_model(model_data: dict, sample_df: pd.DataFrame) -> list:
    """Make prediction with the model"""
    features = model_data['features']
    sample_df = sample_df[features]
    
    sample_df = pd.get_dummies(sample_df, columns=['country'])
    
    missing_cols = set(model_data['model'].feature_names_in_) - set(sample_df.columns)
    for col in missing_cols:
        sample_df[col] = 0
        
    sample_df = sample_df[model_data['model'].feature_names_in_]
    predictions = model_data['model'].predict(sample_df)
    return model_data['label_encoder'].inverse_transform(predictions).tolist()

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Displays the homepage"""
    return """
    <h1>Product Management API</h1>
    <ul>
        <li><a href="/docs">API Documentation</a></li>
        <li><a href="/products">Product List</a></li>
    </ul>
    """

@app.get("/products", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    """Retrieves all products from the database"""
    return db.query(ProductDB).all()

@app.post("/predict")
async def predict(items: ProductItems):
    """Makes prediction based on incoming data"""
    try:
        df = pd.DataFrame([item.dict() for item in items.items])
        df = prepare_sample_data(df)
        predictions = predict_with_model(model_data, df)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Application Launch ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
    
    
'''
To test the API with an example request:
{
  "items": [
    {
      "country": "Switzerland",
      "quantity": 30,
      "unit_price": 44.0,
      "discount": 0,
      "category_id": 4,
      "season": "Summer"
    }
  ]
}'''