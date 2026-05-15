#!/bin/bash

echo "Activating Spark environment..."

source /mnt/c/Users/udhayaprakash.m/Documents/capstone_project/venv_wsl/bin/activate

export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

echo "Running Spark job..."

python /mnt/c/Users/udhayaprakash.m/Documents/capstone_project/spark/telecom_pipeline.py

echo "✅ Spark job completed"
