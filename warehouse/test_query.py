from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///telecom.db")

query = text("""
SELECT r.region_name, t.hour, SUM(f.call_count) AS total_calls
FROM fact_usage f
JOIN dim_time t ON f.time_id = t.time_id
JOIN dim_region r ON f.region_id = r.region_id
GROUP BY r.region_name, t.hour
ORDER BY total_calls DESC
LIMIT 10;
""")

# ✅ Use connection object (correct way)
with engine.connect() as conn:
    result = conn.execute(query)

    for row in result:
        print(row)