import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Database connection
DATABASE_URL = "postgresql://postgres:Silasila.17@localhost:5432/GYK2Northwind"
engine = create_engine(DATABASE_URL)

def load_data(engine):
    """Load all tables from database"""
    tables = ['categories', 'customers', 'order_details', 'orders', 'products']
    data = {}
    
    try:
        with engine.connect() as connection:
            for table in tables:
                data[table] = pd.read_sql_table(table, connection)
        print("Data loaded successfully")
        return data
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None

def check_missing_data(data):
    """Check for missing values in all DataFrames"""
    print("\nMissing data check:")
    for name, df in data.items():
        print(f"{name}:")
        print(df.isnull().sum())
        print("*****")

def clean_data(df):
    """Clean a single DataFrame without chained assignment"""
    df = df.copy()
    
    for col in df.columns:
        # Handle text columns
        if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            # Replace various null representations
            df[col] = df[col].replace(['None', 'nan', 'NaN', 'NULL', 'none', ''], np.nan)
            if df[col].isna().any():
                mode_values = df[col].mode()
                most_frequent = mode_values[0] if not mode_values.empty else ''
                df.loc[:, col] = df[col].fillna(most_frequent)  # Fixed chained assignment
        
        # Handle numeric columns
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isna().any():
                mean_val = df[col].mean()
                df.loc[:, col] = df[col].fillna(mean_val)  # Fixed chained assignment
    
    return df

def update_database(engine, data):
    """Update database tables safely"""
    # Define update order based on foreign key dependencies
    update_order = ['categories', 'products', 'customers', 'orders', 'order_details']
    
    try:
        with engine.begin() as connection:
            # Disable triggers temporarily to avoid constraint issues
            connection.execute(text("SET session_replication_role = 'replica'"))
            
            for table in update_order:
                # Get the DataFrame
                df = data[table]
                
                # Clear existing data
                connection.execute(text(f"TRUNCATE TABLE {table} CONTINUE IDENTITY CASCADE"))
                
                # Insert new data
                df.to_sql(
                    table,
                    con=connection,
                    if_exists='append',
                    index=False,
                    chunksize=1000
                )
                print(f"{table} table updated successfully")
            
            # Re-enable triggers and constraints
            connection.execute(text("SET session_replication_role = 'origin'"))
            
    except SQLAlchemyError as e:
        print(f"Database update failed: {e}")
        return False
    return True

def main():
    # 1. Load data
    data = load_data(engine)
    if data is None:
        return
    
    # 2. Check initial data quality
    check_missing_data(data)
    
    # 3. Clean data
    for name in data:
        data[name] = clean_data(data[name])
    
    # 4. Verify cleaning
    print("\nAfter cleaning - missing values check:")
    check_missing_data(data)
    
    # 5. Update database
    if update_database(engine, data):
        print("\nDatabase update completed successfully!")
    else:
        print("\nDatabase update failed")

if __name__ == "__main__":
    main()
    engine.dispose()