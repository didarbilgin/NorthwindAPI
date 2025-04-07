"""API uç noktalarını oluşturmak için FastAPI kullanılacak. Bu dosya, ürün listeleme, tahmin yapma
ve model eğitme gibi işlevleri sağlayacak."""

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

# --- Veritabanı ve Uygulama Yapılandırması ---
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/northwindapi"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy Modelleri ---
class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    country = Column(String)
    season = Column(String)
    category_id = Column(Integer)

# --- Pydantic Modelleri ---
class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    country: str
    season: str
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

# --- Uygulama Yaşam Döngüsü ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç/kapanış işlemleri"""
    # Başlangıçta veritabanı bağlantısını test et
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✓ PostgreSQL bağlantısı başarılı")
    except Exception as e:
        print(f"✗ PostgreSQL bağlantı hatası: {e}")
    
    # Tabloları oluştur (sadece geliştirme ortamında)
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Kapanış işlemleri (opsiyonel)
    print("Uygulama kapatılıyor...")

app = FastAPI(lifespan=lifespan)

# --- Yardımcı Fonksiyonlar ---
def get_db():
    """Her istek için yeni bir veritabanı oturumu sağlar"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def prepare_sample_data(df: pd.DataFrame) -> pd.DataFrame:
    """Gelen veriyi model için hazırlar"""
    df = df.copy()
    df['total_price'] = df['unit_price'] * df['quantity']
    df['discounted'] = (df['discount'] > 0).astype(int)
    return df

# --- Makine Öğrenmesi Modeli ---
try:
    model_data = pickle.load(open("rf_product_model_simple.pkl", "rb"))
except Exception as e:
    raise RuntimeError(f"Model yüklenemedi: {str(e)}")

def predict_with_model(model_data: dict, sample_df: pd.DataFrame) -> list:
    """Modelle tahmin yapar"""
    features = model_data['features']
    sample_df = sample_df[features]
    
    sample_df = pd.get_dummies(sample_df, columns=['country'])
    
    missing_cols = set(model_data['model'].feature_names_in_) - set(sample_df.columns)
    for col in missing_cols:
        sample_df[col] = 0
        
    sample_df = sample_df[model_data['model'].feature_names_in_]
    predictions = model_data['model'].predict(sample_df)
    return model_data['label_encoder'].inverse_transform(predictions).tolist()

# --- API Endpointleri ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Ana sayfayı gösterir"""
    return """
    <h1>Ürün Yönetim API</h1>
    <ul>
        <li><a href="/docs">API Dokümantasyonu</a></li>
        <li><a href="/products">Ürün Listesi</a></li>
    </ul>
    """

@app.get("/products", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    """Tüm ürünleri veritabanından getirir"""
    return db.query(ProductDB).all()

@app.post("/predict")
async def predict(items: ProductItems):
    """Gelen veriye göre tahmin yapar"""
    try:
        df = pd.DataFrame([item.dict() for item in items.items])
        df = prepare_sample_data(df)
        predictions = predict_with_model(model_data, df)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Uygulama Başlatma ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)