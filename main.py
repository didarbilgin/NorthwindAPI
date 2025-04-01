from database import load_data, check_missing_data, update_database
from data_processing import fill_missing_values
from sqlalchemy import create_engine

def main():
    # Database connection
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/GYK2-Northwind"
    engine = create_engine(DATABASE_URL)
    
    # Load data
    data = load_data(engine)
    if data is None:
        return
    
    #Check initial data quality
    check_missing_data(data)
    
    # fill value
    for name in data:
        data[name] = fill_missing_values(data[name])
    
    # Verify cleaning
    print("\nAfter cleaning - missing values check:")
    check_missing_data(data)
    
    # Update database
    if update_database(engine, data):
        print("\nDatabase update completed successfully!")
    else:
        print("\nDatabase update failed")
    
    engine.dispose()

if __name__ == "__main__":
    main()