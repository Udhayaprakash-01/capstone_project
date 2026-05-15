from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import shutil
import glob
import subprocess
import sys

# ✅ Folder paths
LANDING = "data/landing"
RAW = "data/raw"
REJECTED = "data/rejected"

EXPECTED_COLUMNS = ["datetime", "CellID", "countrycode",
                    "smsin", "smsout", "callin", "callout", "internet"]


# ✅ 1. detect_files
def detect_files(**kwargs):
    files = glob.glob(f"{LANDING}/*.csv")
    print("Detected files:", files)
    return files


# ✅ 2. validate_files
def validate_files(**kwargs):
    files = kwargs['ti'].xcom_pull(task_ids='detect_files')

    valid_files = []
    invalid_files = []

    for file in files:
        with open(file, 'r') as f:
            header = f.readline().strip().split(',')

            if header == EXPECTED_COLUMNS:
                valid_files.append(file)
            else:
                invalid_files.append(file)

    print("Valid:", valid_files)
    print("Invalid:", invalid_files)

    return {"valid": valid_files, "invalid": invalid_files}


# ✅ 3. move_files
def move_files(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='validate_files')

    valid_files = data["valid"]
    invalid_files = data["invalid"]

    for file in valid_files:
        shutil.move(file, RAW)

    for file in invalid_files:
        shutil.move(file, REJECTED)

    print("Files moved successfully")


# ✅ 4. log_status
def log_status():
    print("File validation and movement completed ✅")


# ✅ 5. run_spark_job
def run_spark_job():
    import subprocess

    try:
        print("Running Spark pipeline via script...")

        subprocess.run(
            ["/bin/bash", "/mnt/c/Users/udhayaprakash.m/Documents/capstone_project/run_spark.sh"],
            check=True
        )

        print("✅ Spark job completed successfully")

    except Exception as e:
        print("Spark job failed ❌", e)
        raise


# ✅ 6. load_warehouse
def load_warehouse():
    print("Loading data into warehouse...")
    # will implement in Task 3.4
    pass


# ✅ 7. notify
def notify():
    print("✅ Pipeline completed successfully!")


# ✅ DAG Definition
with DAG(
    dag_id="telecom_pipeline_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    dagrun_timeout=timedelta(minutes=30)
) as dag:

    t1 = PythonOperator(
        task_id="detect_files",
        python_callable=detect_files
    )

    t2 = PythonOperator(
        task_id="validate_files",
        python_callable=validate_files
    )

    t3 = PythonOperator(
        task_id="move_files",
        python_callable=move_files
    )

    t4 = PythonOperator(
        task_id="log_status",
        python_callable=log_status
    )

    t5 = PythonOperator(
        task_id="run_spark_job",
        python_callable=run_spark_job
    )

    t6 = PythonOperator(
        task_id="load_warehouse",
        python_callable=load_warehouse
    )

    t7 = PythonOperator(
        task_id="notify",
        python_callable=notify
    )

    # ✅ Task Pipeline
    t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7