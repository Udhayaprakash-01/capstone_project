from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
import pandas as pd
from ml.predict import predict_usage_risk

app = FastAPI(title="Telecom API")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ✅ MYSQL CONNECTION (UPDATED ✅)
engine = create_engine("mysql+pymysql://root:root@localhost/telecom_db")


# =========================
# ✅ MODELS
# =========================

class SummaryResponse(BaseModel):
    total_calls: int
    total_sms: int
    total_internet_mb: float
    peak_hour: int
    busiest_region: str


class RegionUsage(BaseModel):
    region: str
    hourly_distribution: list
    trend: list


class PeakResponse(BaseModel):
    top_hours: list
    top_regions: list


class FeatureResponse(BaseModel):
    region: str
    avg_usage: float
    growth_rate: float
    variability: float
    peak_ratio: float


class PredictionRequest(BaseModel):
    region: str
    avg_usage: float
    growth_rate: float
    variability: float


class PredictionResponse(BaseModel):
    congestion_risk: str
    anomaly_flag: bool
    score: float


# =========================
# ✅ API 1 — SUMMARY
# =========================

@app.get("/usage/summary", response_model=SummaryResponse)
def get_summary():
    try:
        df = pd.read_sql("SELECT * FROM fact_usage", engine)

        total_calls = int(df["call_count"].sum())
        total_sms = int(df["sms_count"].sum())
        total_internet = float(df["internet_mb"].sum())

        # ✅ Peak hour
        hourly = pd.read_sql("""
            SELECT t.hour, SUM(f.call_count) AS total_calls
            FROM fact_usage f
            JOIN dim_time t ON f.time_id = t.time_id
            GROUP BY t.hour
            ORDER BY total_calls DESC
            LIMIT 1
        """, engine)

        peak_hour = int(hourly.iloc[0]["hour"])

        # ✅ Busiest region
        region = pd.read_sql("""
            SELECT r.region_name, SUM(f.call_count) AS total_calls
            FROM fact_usage f
            JOIN dim_region r ON f.region_id = r.region_id
            GROUP BY r.region_name
            ORDER BY total_calls DESC
            LIMIT 1
        """, engine)

        busiest_region = str(region.iloc[0]["region_name"])

        return {
            "total_calls": total_calls,
            "total_sms": total_sms,
            "total_internet_mb": total_internet,
            "peak_hour": peak_hour,
            "busiest_region": busiest_region
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ✅ API 2 — REGION USAGE
# =========================
@app.get("/usage/region/{region}", response_model=RegionUsage)
def region_usage(region: str):
    try:

        query = f"""
        SELECT 
            t.hour,
            SUM(f.call_count) AS call_count,
            SUM(f.sms_count) AS sms_count,
            SUM(f.internet_mb) AS internet_mb
        FROM fact_usage f
        JOIN dim_time t ON f.time_id = t.time_id
        JOIN dim_region r ON f.region_id = r.region_id
        WHERE LOWER(r.region_name) = LOWER('{region}')
        GROUP BY t.hour
        ORDER BY t.hour
        """

        df = pd.read_sql(query, engine)

        if df.empty:
            raise HTTPException(status_code=404, detail="Region not found")

        hourly = df.to_dict(orient="records")

        return {
            "region": region,
            "hourly_distribution": hourly,
            "trend": hourly
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# ✅ API 3 — PEAK TRAFFIC
# =========================
@app.get("/usage/peak", response_model=PeakResponse)
def peak_usage():
    try:

        top_hours = pd.read_sql("""
            SELECT 
                t.hour,
                SUM(f.call_count + f.sms_count + f.internet_mb) AS total_usage
            FROM fact_usage f
            JOIN dim_time t ON f.time_id = t.time_id
            GROUP BY t.hour
            ORDER BY total_usage DESC
            LIMIT 5
        """, engine).to_dict(orient="records")

        top_regions = pd.read_sql("""
            SELECT 
                r.region_name AS region,
                SUM(f.call_count + f.sms_count + f.internet_mb) AS total_usage
            FROM fact_usage f
            JOIN dim_region r ON f.region_id = r.region_id
            GROUP BY r.region_name
            ORDER BY total_usage DESC
            LIMIT 5
        """, engine).to_dict(orient="records")

        return {
            "top_hours": top_hours,
            "top_regions": top_regions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ✅ API 4 — FEATURES
# =========================

@app.get("/usage/features/{region}", response_model=FeatureResponse)
def features(region: str):
    try:

        df = pd.read_sql(f"""
            SELECT f.internet_mb
            FROM fact_usage f
            JOIN dim_region r ON f.region_id = r.region_id
            WHERE LOWER(r.region_name) = LOWER('{region}')
        """, engine)

        if df.empty:
            raise HTTPException(status_code=404, detail="Region not found")

        avg_usage = float(df["internet_mb"].mean())
        variability = float(df["internet_mb"].std())
        peak_ratio = float(df["internet_mb"].max() / avg_usage)
        growth_rate = 0.1   # simple placeholder

        return {
            "region": region,
            "avg_usage": avg_usage,
            "growth_rate": growth_rate,
            "variability": variability,
            "peak_ratio": peak_ratio
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ✅ API 5 — PREDICTION
# =========================

@app.post("/predict-usage-risk", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    try:
        features = {
            "avg_usage": req.avg_usage,
            "growth_rate": req.growth_rate,
            "variability": req.variability,
            "peak_ratio": 1.2
        }

        result = predict_usage_risk(features)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))