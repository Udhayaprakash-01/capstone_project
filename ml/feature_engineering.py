import pandas as pd
from sqlalchemy import create_engine

# ✅ Use MySQL instead of SQLite
engine = create_engine("mysql+pymysql://root:root@localhost/telecom_db")


def build_features():

    df = pd.read_sql("""
        SELECT f.*, r.region_name
        FROM fact_usage f
        JOIN dim_region r ON f.region_id = r.region_id
    """, engine)

    features = []

    for region, group in df.groupby("region_name"):

        group = group.sort_values("time_id")

        # ✅ Average usage
        avg_usage = group["internet_mb"].mean()

        # ✅ Variability
        variability = group["internet_mb"].std()

        # ✅ Growth rate (REAL CALCULATION ✅)
        if len(group) > 1:
            growth_rate = (group["internet_mb"].iloc[-1] - group["internet_mb"].iloc[0]) / group["internet_mb"].iloc[0]
        else:
            growth_rate = 0.0

        # ✅ Peak ratio
        peak_ratio = group["internet_mb"].max() / avg_usage

        features.append({
            "region": region,
            "avg_usage": float(avg_usage),
            "growth_rate": float(growth_rate),
            "variability": float(variability),
            "peak_ratio": float(peak_ratio)
        })

    return pd.DataFrame(features)


if __name__ == "__main__":
    print(build_features())
