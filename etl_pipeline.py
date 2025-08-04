# Import Libraries
import pandas as pd # for data manipulation/extraction/transformation/loading/analysis
import psycopg2 # for PostgreSQL database connection
from sqlalchemy import create_engine #for SQLAlchemy connection to PostgreSQL
from db_config import db_username, db_password, db_host, db_port, db_name, csv_file_path

#Step 1: Load the CSV file into a DataFrame
data = pd.read_csv(csv_file_path)

#step 2: Transform the data (cleaning, duplicates, missing values, etc.)
check_dup = data.duplicated().sum() # Check for duplicates
if check_dup > 0:
    data = data.drop_duplicates(keep='first', inplace=True) # Drop duplicates if any and keep the first occurrence

# Check for missing values
missing_values = data.isnull()
# Taking a look of the missing values data
missing_education_data = data[data['education'].isnull()].head(5) # Display the first 10 rows with missing values in the 'education' column
missing_rating_data = data[data['previous_year_rating'].isnull()].head(5) # Display the first 10 rows with missing values in the 'previous_year_rating' column

# Fill missing education values
data['education'] = data['education'].fillna('Not Specified')

# Fill missing rating values
data['previous_year_rating'] = data['previous_year_rating'].fillna(0)

missing_values = data.isnull()
print(missing_values.sum())

# Step 3: Load the DataFrame into a PostgreSQL database
# Database credentials
db_username = 'postgres'
db_password = 'Dora%401970%2E'
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'

# Create a connection string
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
print("Connection to PostgreSQL database established successfully.")

# Load the DataFrame into a PostgreSQL table
data.to_sql('emp_table', engine, if_exists='replace', index=False)
print("Data loaded into PostgreSQL table 'emp_table' successfully.")
engine.dispose()  # Close the connection
print("Connection to PostgreSQL database closed.")
# End of the ETL process
print("ETL process completed successfully.")