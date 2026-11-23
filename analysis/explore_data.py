import pandas as pd

# Load ONE enrollment file
df = pd.read_csv('../data/api_data_aadhar_enrolment/api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv')

# Show first 5 rows
print("First 5 rows:")
print(df.head())

# Show basic info
print("\n📊 Dataset Info:")
print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Show data types
print("\n📋 Column Types:")
print(df.dtypes)

# Check for missing values
print("\n❓ Missing Values:")
print(df.isnull().sum())    