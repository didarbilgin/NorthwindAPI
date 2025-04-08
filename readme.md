# Product Recommendation & Analysis API with FastAPI

This repository contains a complete machine learning pipeline and API built using **FastAPI** and **PostgreSQL**, designed for product prediction and sales analysis based on customer orders.

---

## Features

- List products from the database (`GET /products`)
- Predict most likely product ID using trained Random Forest (`POST /predict`)
- Automatically handle missing values in database tables
- Clean and transform data with feature engineering
- Visualize key metrics such as customer distribution, product sales, seasonal trends
- Analyze and generate interactive reports (heatmap, pie, bar, line charts)
- Train and evaluate Random Forest model using real order data

---

## Project Structure

```
.
├── main.py                   # FastAPI app with /products and /predict endpoints
├── data_processing.py        # Missing value handling and feature engineering
├── database.py               # Database query and update logic
├── prepare_and_update.py     # Runs full ETL: fetch, clean, update DB
├── train_model.py            # Model training script (Random Forest)
├── test_model.py             # Predict using the trained model
├── rf_product_model_simple.pkl  # Trained model file
├── label_encoder.pkl         # Label encoder for product IDs
├── data_visualizations.py    # Pie, bar, line, choropleth charts
├── requirements.txt
└── README.md
```

---

## Technologies Used

- **FastAPI** – Web framework for serving ML models
- **SQLAlchemy** – ORM for PostgreSQL interaction
- **scikit-learn** – For building and saving the ML model
- **matplotlib / seaborn / plotly** – For data visualization
- **Pandas / NumPy** – Data wrangling and transformation

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Server

```bash
uvicorn api:app --reload
```

Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### `GET /products`

**Description:**  
Returns the full list of products from the `products` table.

**Response:**

```json
[
  {
    "product_id": 1,
    "product_name": "Chai",
    "unit_price": 18.0,
    "units_in_stock": 39,
    "category_id": 1
  },
  ...
]
```

---

### `POST /predict`

**Description:**  
Predicts the product based on the input features using trained RandomForest.

**Request:**

```json
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
}
```

**Response:**

```json
{
  "predictions": ["59"]
}
```

---

## Sample Visualizations

- **Choropleth map** of quantity by country
- **Pie charts** of:
- Customer distribution by country
- Product sales by season
- Product ID distribution
- **Bar chart** of top 20 customers by total sales
- **Line chart** for monthly sales trends over time

---

## Postman & Swagger

- Swagger docs available at `/docs`
- To test manually in Postman:
  - Set `Content-Type: application/json`
  - Use the same structure shown in the sample requests above

---

## Future Improvements

- [ ] Create Dockerfile for deployment
- [ ] Add endpoint for model retraining (`POST /retrain`)
- [ ] CI/CD with GitHub Actions

---

## Author

Developed by Didar Nur Bilgin, Sezin Acet, Sıla Durtaş, Yağmur Özcan, Zeynep Öztürk / Pair 2
Feel free to open an issue or contribute via pull request.
