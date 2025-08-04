# Import Libraries
import pandas as pd # for data manipulation/extraction/transformation/loading/analysis
from sqlalchemy import create_engine #for SQLAlchemy connection to PostgreSQL
from db_config import db_username, db_password, db_host, db_port, db_name, csv_file_path

#Step 1: Ectract
def extract_data():
    print("Starting data extraction from CSV...")
    data = pd.read_csv(csv_file_path)
    print(f"ata extracted. Shape: {data.shape}")
    return data

#step 2: Transform the data (cleaning, duplicates, missing values, etc.)
def transform_data(data):
    print("Transforming data...")
    
    check_dup = data.duplicated().sum() # Check for duplicates
    if check_dup > 0:
        data = data.drop_duplicates(keep='first', inplace=True) # Drop duplicates if any and keep the first occurrence
        print(f"Duplicates found and removed: {check_dup}")
        
    # Check for missing values
    missing_values = data.isnull()
    # Fill missing education values
    data['education'] = data['education'].fillna('Not Specified')

    # Fill missing rating values
    data['previous_year_rating'] = data['previous_year_rating'].fillna(0)

    missing_values = data.isnull()
    print(missing_values.sum())
    
    return data

# Step 3: Load the DataFrame into a PostgreSQL database
def load_data(data):
    print("Loading data into PostgreSQL...")

    engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    print("Connection to PostgreSQL database established successfully.")

    # Fix: Use `engine.connect()` to get a real SQLAlchemy connection
    with engine.connect() as connection:
        data.to_sql(
            'emp_table',
            con=connection,
            if_exists='replace',
            index=False,
            method='multi'
        )

    print("Data loaded into PostgreSQL table 'emp_table' successfully.")
    engine.dispose()
    print("Connection to PostgreSQL database closed.")
    
def run_etl():
    data = extract_data()  # Step 1: Extract
    transformed_data = transform_data(data)  # Step 2: Transform
    load_data(transformed_data)  # Step 3: Load
    print("ETL process completed successfully.")

if __name__ == "__main__":
    run_etl()