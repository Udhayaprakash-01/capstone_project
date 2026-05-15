import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@localhost/telecom_db")

print("Loading processed data...")

# ✅ Load parquet
df = pd.read_parquet("data/processed/telecom_data")

# ✅ Create time_id (unique per row)
df['time_id'] = range(1, len(df) + 1)

# ✅ ✅ FIXED REGION MAPPING (IMPORTANT ✅)
def assign_region(grid_id):
    if grid_id < 2000:
        return "Region_A"
    elif grid_id < 4000:
        return "Region_B"
    else:
        return "Region_C"

df['region_name'] = df['grid_id'].apply(assign_region)

# ======================================================
# ✅ DIM_TIME
# ======================================================
dim_time = df[['time_id', 'day', 'hour']].copy()
dim_time['date'] = pd.to_datetime(dim_time['day'])
dim_time['month'] = dim_time['date'].dt.month
dim_time['weekday'] = dim_time['date'].dt.day_name()
dim_time['day'] = dim_time['date'].dt.day

dim_time = dim_time[['time_id', 'date', 'hour', 'day', 'month', 'weekday']]

# ======================================================
# ✅ DIM_REGION (FIXED ✅)
# ======================================================
dim_region = df[['region_name']].drop_duplicates().copy()
dim_region['region_id'] = range(1, len(dim_region) + 1)
dim_region['city'] = "Milan"

# ✅ Merge region_id back into df (IMPORTANT ✅)
df = df.merge(dim_region, on="region_name")

# ======================================================
# ✅ FACT TABLE
# ======================================================
fact = df[['time_id', 'region_id', 'call_count', 'sms_count', 'internet_usage']].copy()
fact['usage_id'] = range(1, len(fact) + 1)

fact.rename(columns={'internet_usage': 'internet_mb'}, inplace=True)

# ======================================================
# ✅ CLEAN EXISTING DATA (IMPORTANT ✅)
# ======================================================
from sqlalchemy import text  # ✅ ADD THIS IMPORT

with engine.begin() as conn:
    conn.execute(text("DELETE FROM fact_usage"))
    conn.execute(text("DELETE FROM dim_time"))
    conn.execute(text("DELETE FROM dim_region"))

# ======================================================
# ✅ LOAD TO DATABASE
# ======================================================
dim_time.to_sql('dim_time', engine, if_exists='append', index=False)
dim_region.to_sql('dim_region', engine, if_exists='append', index=False)
fact.to_sql('fact_usage', engine, if_exists='append', index=False)

print("✅ Warehouse loaded successfully ✅")
