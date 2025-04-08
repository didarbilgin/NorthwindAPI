from database import fetch_data, check_missing_values, update_database, DATABASE_URL, engine, categorize_columns
from data_processing import fill_missing_values
from sqlalchemy import create_engine


# Main function that manages all operations: fetches data, fills missing values, and updates the database.
def main():
    try:
        tables = ["categories", "products", "customers", "orders", "order_details"]
        processed_data = {}
        
        for table in tables:
            print(f"==> Processing {table} Table <==")
            df = fetch_data(f"SELECT * FROM {table}")
            
            check_missing_values(df, table)
            numeric_cols, text_cols = categorize_columns(df, table)
            df = fill_missing_values(df, numeric_cols, text_cols, table)
            
            check_missing_values(df, table)
            processed_data[table] = df
            print(f"{table} table completed.\n{'=' * 40}\n")
        
        # Update the database
        if update_database(engine, processed_data):
            print("Database update completed successfully!")
        else:
            print("An error occurred while updating the database!")
        
    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    main()