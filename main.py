from database import fetch_data, check_missing_values, update_database,DATABASE_URL,engine,categorize_columns
from data_processing import fill_missing_values
from sqlalchemy import create_engine


    # Tüm işlemleri yöneten ana fonksiyon. Verileri çeker, eksik değerleri doldurur ve veritabanını günceller.
def main():
    try:
        tables = ["categories", "products", "customers", "orders", "order_details"]
        processed_data = {}
        
        for table in tables:
            print(f"==> {table} Tablosu İşleniyor <==")
            df = fetch_data(f"SELECT * FROM {table}")
            
            check_missing_values(df, table)
            numeric_cols, text_cols = categorize_columns(df, table)
            df = fill_missing_values(df, numeric_cols, text_cols, table)
            
            check_missing_values(df, table)
            processed_data[table] = df
            print(f"{table} tablosu tamamlandı.\n{'=' * 40}\n")
        
        # Veritabanını günceller.
        if update_database(engine, processed_data):
            print("Tüm veritabanı güncellemesi başarıyla tamamlandı!")
        else:
            print("Veritabanı güncellemesinde hata oluştu!")
        
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    main()
