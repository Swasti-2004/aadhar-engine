import pandas as pd
import os

# 1. Merge all ENROLLMENT files
print("📁 Merging Enrollment files...")
enrolment_files = [
    '../data/api_data_aadhar_enrolment/api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv',
    '../data/api_data_aadhar_enrolment/api_data_aadhar_enrolment/api_data_aadhar_enrolment_500000_1000000.csv',
    '../data/api_data_aadhar_enrolment/api_data_aadhar_enrolment/api_data_aadhar_enrolment_1000000_1006029.csv'
]

df_enrolment = pd.concat([pd.read_csv(f) for f in enrolment_files], ignore_index=True)
print(f"✅ Total enrollment records: {len(df_enrolment)}")

# Save merged file
df_enrolment.to_csv('enrolment_merged.csv', index=False)
print("✅ Saved: enrolment_merged.csv\n")



# 2. Merge all DEMOGRAPHIC files
print("📁 Merging Demographic files...")

# First, let's check what files exist
demo_folder = '../data/api_data_aadhar_demographic/api_data_aadhar_demographic/'
demo_files = []

# Add the file patterns you have
for i in range(0, 2500000, 500000):
    if i == 0:
        file_path = f'{demo_folder}api_data_aadhar_demographic_{i}_500000.csv'
    else:
        file_path = f'{demo_folder}api_data_aadhar_demographic_{i}_{i+500000}.csv'
    
    if os.path.exists(file_path):
        demo_files.append(file_path)
        print(f"  Found: {file_path}")

df_demographic = pd.concat([pd.read_csv(f) for f in demo_files], ignore_index=True)
print(f"✅ Total demographic records: {len(df_demographic)}")

# Save merged file
df_demographic.to_csv('demographic_merged.csv', index=False)
print("✅ Saved: demographic_merged.csv\n")


# 3. Merge all BIOMETRIC files
print("📁 Merging Biometric files...")

bio_folder = '../data/api_data_aadhar_biometric/api_data_aadhar_biometric/'
bio_files = []

# Add the file patterns you have
for i in range(0, 2000000, 500000):
    if i == 0:
        file_path = f'{bio_folder}api_data_aadhar_biometric_{i}_500000.csv'
    else:
        file_path = f'{bio_folder}api_data_aadhar_biometric_{i}_{i+500000}.csv'
    
    if os.path.exists(file_path):
        bio_files.append(file_path)
        print(f"  Found: {file_path}")

df_biometric = pd.concat([pd.read_csv(f) for f in bio_files], ignore_index=True)
print(f"✅ Total biometric records: {len(df_biometric)}")

# Save merged file
df_biometric.to_csv('biometric_merged.csv', index=False)
print("✅ Saved: biometric_merged.csv\n")

print("🎉 ALL FILES MERGED SUCCESSFULLY!")
print(f"📊 Summary:")
print(f"  - Enrollment: {len(df_enrolment):,} records")
print(f"  - Demographic: {len(df_demographic):,} records")
print(f"  - Biometric: {len(df_biometric):,} records")