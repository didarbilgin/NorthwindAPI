import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np

"""This file allows you to connect to a PostgreSQL database and contains functions for data retrieval."""
# load_data update_database check_missing_data

# Establish PostgreSQL database connection.
DATABASE_URL = "postgresql://postgres:Silasila.17@localhost:5432/GYK2Northwind"
engine = create_engine(DATABASE_URL)

# Executes the given SQL query and returns the result as a DataFrame.
def fetch_data(query):
    print(f"Running query: {query}")
    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection)
    df.replace("[null]", np.nan, inplace=True)  # Replaces '[null]' values with NaN.
    
    print(f"Initial data loaded:\n{df.head()}\n{'-' * 20}\n")
    return df

# Checks for missing values in the DataFrame and prints the result.
def check_missing_values(df, table_name):
    print(f"Checking for missing values in {table_name} table...")
    missing = df.isnull().sum()
    print(f"Missing values:\n{missing}\n{'-' * 20}\n")

# Separates numeric and text columns in the DataFrame and prints them.
def categorize_columns(df, table_name):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()

    if 'picture' in text_cols:  # Removes the 'picture' column from text columns.
        text_cols.remove('picture')
    print(f"Numeric columns in {table_name} table: {numeric_cols}")
    print(f"Text columns in {table_name} table: {text_cols}\n{'-' * 20}\n")
    return numeric_cols, text_cols

def update_database(engine, data):
    """Safely updates the database tables."""
    update_order = ['categories', 'products', 'customers', 'orders', 'order_details']  
    try:
        with engine.begin() as connection:
            # Temporarily disables foreign key checks.
            connection.execute(text("SET session_replication_role = 'replica'"))
            for table in update_order:
                df = data[table]
                
                # Truncates the table (keeps ID sequence intact).
                connection.execute(text(f"TRUNCATE TABLE {table} CONTINUE IDENTITY CASCADE"))
                
                # Reloads data into the table.
                df.to_sql(table, con=connection, if_exists='append', index=False, chunksize=1000)
                print(f"{table} table updated successfully.")
            
            # Reactivates foreign key checks.
            connection.execute(text("SET session_replication_role = 'origin'"))
        
    except Exception as e:
        print(f"Database update failed: {e}")
        return False
    return True


