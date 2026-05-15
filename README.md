Telecom Network Intelligence System

📌 Overview
The Telecom Network Intelligence System is an end-to-end data engineering and analytics platform designed to process, analyze, and predict telecom network activity. The system handles high-volume telecom datasets (CDR, SMS, and internet traffic) and provides real-time insights along with machine learning–based congestion risk predictions.
This project demonstrates a complete data pipeline architecture, integrating distributed data processing, workflow orchestration, data warehousing, backend APIs, frontend dashboards, and machine learning.

Architecture:

Data Sources (CSV)
        ↓
Airflow Orchestration (DAG)
        ↓
Raw Layer (CSV)
        ↓
Spark Processing (ETL)
        ↓
Processed Layer (Parquet)
        ↓
SQL Data Warehouse (Star Schema)
        ↓
FastAPI Backend (REST APIs)
        ↓
React Frontend Dashboard
        ↓
Machine Learning (Prediction Layer)


Tech Stack:

Data Engineering

PySpark – Distributed data processing
Apache Airflow – Workflow orchestration
SQL (SQLite/PostgreSQL/MySQL) – Data warehousing

2. Backend

FastAPI – REST API layer
Pydantic – Data validation
SQLAlchemy – Database interaction

3. Frontend

React (Vite) – UI dashboard
Axios – API integration

4. Machine Learning

Scikit-learn – Model training
Joblib – Model persistence


Features:

-> Data Pipeline

Ingest telecom CSV data
Validate and filter datasets
Perform distributed ETL using PySpark
Store data in optimized Parquet format

-> Data Warehouse (Star Schema)

1.fact_usage
2.dim_time
3.dim_region

Supports analytical queries such as:

SELECT r.region_name, t.hour, SUM(f.call_count)
FROM fact_usage f
JOIN dim_time t ON f.time_id = t.time_id
JOIN dim_region r ON f.region_id = r.region_id;

-> REST APIs (FastAPI)

    Endpoint                          Description
/usage/summary                    Overall usage metrics
/usage/region/{region}            Region-level usage
/usage/peak                       Peak traffic insights
/usage/features/{region}          ML feature extraction
/predict-usage-risk               ML-based congestion prediction

-> React Dashboard

Usage Dashboard → KPI metrics
Region Explorer → Hourly usage analysis
Peak Traffic    → Top usage trends
Risk Prediction → ML-driven predictions


-> Machine Learning

Problem
Predict telecom network congestion risk

Features
Average usage
Growth rate
Peak ratio
Variability

Model
Random Forest Classifier

Output
{  
"congestion_risk": "HIGH",  
"anomaly_flag": true,  
"score": 0.92
}

-> Batch Scoring

Generate predictions for all regions:
python ml/batch_score.py

Output:
ml/batch_predictions.csv

Project Structure:

capstone_project/
│
├── data/
│   ├── landing/
│   ├── raw/
│   ├── processed/
│
├── spark/
│   └── telecom_pipeline.py
│
├── airflow/
│   └── dags/
│       └── telecom_dag.py
│
├── warehouse/
│   ├── schema.sql
│   └── load_warehouse.py
│
├── api/
│   └── main.py
│
├── ml/
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── predict.py
│   ├── batch_score.py
│   └── model.pkl
│
├── react-app/
│
└── docs/
    ├── architecture-diagram.png
    └── design_document.md


How to Run:

1️⃣ Backend (FastAPI)
uvicorn api.main:app --reload

Open:
http://127.0.0.1:8000/docs


2️⃣ Frontend (React)
cd react-app
npm install
npm run dev

Open:
http://localhost:5173


3️⃣ Train ML Model
python ml/train_model.py


4️⃣ Batch Predictions
python ml/batch_score.py

Key Highlights:

✅ End-to-end data pipeline
✅ Scalable Spark processing
✅ Airflow orchestration
✅ Star schema warehouse
✅ Production-ready FastAPI APIs
✅ Interactive React dashboard
✅ ML-based prediction layer

Use Cases:

Telecom traffic monitoring
Network congestion detection
Predictive analytics
Capacity planning

Author:

Udhaya Prakash M
Data Engineering & Analytics Enthusiast

Final Note:

This project demonstrates a production-grade data engineering pipeline combined with full-stack development and machine learning, showcasing the ability to design, build, and deploy scalable data systems.