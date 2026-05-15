from usage_processor import UsageProcessor, call_plan_api

processor = UsageProcessor()

# ✅ FIXED PATH
processor.load_data("data/landing")

processor.clean_data()

print("\nDaily Usage:")
print(processor.compute_daily_usage().head())

kpis = processor.compute_kpis()

print("\nPeak Hour:", kpis['peak_hour'])

print("\nRegion Usage Sample:")
print(kpis['region_usage'].head())

print("\nAPI Response:")
print(call_plan_api(101))