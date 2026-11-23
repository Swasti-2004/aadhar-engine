import pandas as pd

# Load merged files
print("📂 Loading data...")
df_enrol = pd.read_csv('enrolment_merged.csv')
df_demo = pd.read_csv('demographic_merged.csv')
df_bio = pd.read_csv('biometric_merged.csv')

print("✅ Data loaded!\n")

# === ANALYSIS 1: Which states have HIGHEST enrollments? ===
print("=" * 50)
print("📍 TOP 10 STATES - ENROLLMENT")
print("=" * 50)
state_enrol = df_enrol.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
state_enrol['total'] = state_enrol.sum(axis=1)
state_enrol = state_enrol.sort_values('total', ascending=False).head(10)
print(state_enrol)
print()



# === ANALYSIS 2: Age Group Distribution ===
print("=" * 50)
print("👶 AGE GROUP DISTRIBUTION - ENROLLMENT")
print("=" * 50)
age_totals = {
    'Babies (0-5)': df_enrol['age_0_5'].sum(),
    'Children (5-17)': df_enrol['age_5_17'].sum(),
    'Adults (18+)': df_enrol['age_18_greater'].sum()
}

for age_group, count in age_totals.items():
    percentage = (count / sum(age_totals.values())) * 100
    print(f"{age_group}: {count:,} ({percentage:.1f}%)")
print()

# === ANALYSIS 3: Demographic vs Biometric Updates ===
print("=" * 50)
print("🔄 UPDATES COMPARISON")
print("=" * 50)
demo_total = df_demo[['demo_age_5_17', 'demo_age_17_']].sum().sum()
bio_total = df_bio[['bio_age_5_17', 'bio_age_17_']].sum().sum()

print(f"Total Demographic Updates: {demo_total:,}")
print(f"Total Biometric Updates: {bio_total:,}")
print(f"Ratio (Demo/Bio): {demo_total/bio_total:.2f}x")


# === ANALYSIS 4: Time-based Trends ===
print("=" * 50)
print("📅 ENROLLMENT TRENDS OVER TIME")
print("=" * 50)

# Convert date to datetime
df_enrol['date'] = pd.to_datetime(df_enrol['date'], format='%d-%m-%Y')
df_enrol['month'] = df_enrol['date'].dt.to_period('M')

# Group by month
monthly = df_enrol.groupby('month')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
monthly['total'] = monthly.sum(axis=1)

print(monthly)
print()

# Find peak day
print("🔥 BUSIEST ENROLLMENT DAY:")
daily = df_enrol.groupby('date')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
daily['total'] = daily.sum(axis=1)
busiest_day = daily['total'].idxmax()
busiest_count = daily['total'].max()
print(f"Date: {busiest_day.strftime('%d-%m-%Y')}")
print(f"Enrollments: {busiest_count:,}")


# === ANALYSIS 5: Top Districts ===
print("=" * 50)
print("📍 TOP 15 DISTRICTS - ENROLLMENT")
print("=" * 50)

district_enrol = df_enrol.groupby(['state', 'district'])[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
district_enrol['total'] = district_enrol.sum(axis=1)
district_enrol = district_enrol.sort_values('total', ascending=False).head(15)
print(district_enrol)
print()

# === ANALYSIS 6: Update Patterns by State ===
print("=" * 50)
print("🔄 TOP 10 STATES - DEMOGRAPHIC UPDATES")
print("=" * 50)

state_demo = df_demo.groupby('state')[['demo_age_5_17', 'demo_age_17_']].sum()
state_demo['total'] = state_demo.sum(axis=1)
state_demo = state_demo.sort_values('total', ascending=False).head(10)
print(state_demo)


# === ANALYSIS 7: Child vs Adult Patterns ===
print("=" * 50)
print("👶 vs 👨 CHILD VS ADULT UPDATE BEHAVIOR")
print("=" * 50)

# Biometric updates by age
bio_child = df_bio['bio_age_5_17'].sum()
bio_adult = df_bio['bio_age_17_'].sum()

# Demo updates by age
demo_child = df_demo['demo_age_5_17'].sum()
demo_adult = df_demo['demo_age_17_'].sum()

print(f"BIOMETRIC Updates:")
print(f"  Children (5-17): {bio_child:,} ({bio_child/(bio_child+bio_adult)*100:.1f}%)")
print(f"  Adults (17+): {bio_adult:,} ({bio_adult/(bio_child+bio_adult)*100:.1f}%)")
print()
print(f"DEMOGRAPHIC Updates:")
print(f"  Children (5-17): {demo_child:,} ({demo_child/(demo_child+demo_adult)*100:.1f}%)")
print(f"  Adults (17+): {demo_adult:,} ({demo_adult/(demo_child+demo_adult)*100:.1f}%)")
print()

print("=" * 50)
print("✅ ANALYSIS COMPLETE!")
print("=" * 50)
