from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
import glob


# ✅ 1. Create Spark Session (optimized for local)
def create_session():
    spark = SparkSession.builder \
        .appName("Telecom Pipeline") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.default.parallelism", "4") \
        .getOrCreate()
    return spark


# ✅ 2. Load Data
def load(spark):

    schema = StructType([
        StructField("datetime", StringType(), True),
        StructField("CellID", IntegerType(), True),
        StructField("countrycode", IntegerType(), True),
        StructField("smsin", DoubleType(), True),
        StructField("smsout", DoubleType(), True),
        StructField("callin", DoubleType(), True),
        StructField("callout", DoubleType(), True),
        StructField("internet", DoubleType(), True)
    ])

    # ✅ In production, Spark reads from RAW layer after Airflow ingestion
    base_path = os.path.abspath("data/raw")

    # ✅ Get files safely (Windows fix)
    files = glob.glob(base_path + "/sms-call-internet-mi-*.csv")

    # ✅ Limit for local run
    files = files[:2]

    print("Files being loaded:", files)

    if len(files) == 0:
        raise Exception("No telecom files found!")

    df = spark.read.csv(files, header=True, schema=schema)

    # ✅ LIMIT EARLY (CRITICAL FIX)
    df = df.limit(200000)   # take only 2 lakh rows BEFORE any heavy processing

    print("Sample Records Count:", df.count())

    print("Total Records:", df.count())

    return df


# ✅ 3. Clean Data
def clean(df):

    df = df.withColumnRenamed("datetime", "timestamp") \
        .withColumnRenamed("CellID", "grid_id") \
        .withColumnRenamed("internet", "internet_usage")

    # ✅ Convert timestamp
    df = df.withColumn("timestamp", to_timestamp("timestamp"))

    # ✅ Create metrics
    df = df.withColumn("call_count", col("callin") + col("callout")) \
           .withColumn("sms_count", col("smsin") + col("smsout"))

    # ✅ Filter bad data
    df = df.filter(
        (col("internet_usage") >= 0) &
        (col("call_count").isNotNull())
    )

    # ✅ Extract features
    df = df.withColumn("hour", hour(col("timestamp"))) \
           .withColumn("day", to_date(col("timestamp")))

    return df


# ✅ 4. Enrich Data (Broadcast Join)
def enrich(df, spark):

    mapping_data = [
        (1, "Region_A", "Milan"),
        (2, "Region_B", "Milan"),
        (3, "Region_C", "Milan")
    ]

    mapping_df = spark.createDataFrame(mapping_data, ["grid_id", "region_name", "city"])

    # ✅ Broadcast join (small dataset → avoids shuffle)
    df = df.join(broadcast(mapping_df), on="grid_id", how="left")

    return df


# ✅ 5. Optimize (lightweight for local)
def optimize(df):

    # ✅ no Repartition safely

    # ✅ Keep only necessary columns
    df = df.select(
        "grid_id",
        "timestamp",
        "call_count",
        "sms_count",
        "internet_usage",
        "hour",
        "day",
        "region_name"
    )

    print("Execution Plan:")
    df.explain()

    return df


# ✅ 6. Aggregations
def aggregate(df):

    calls_per_hour = df.groupBy("hour").agg(
        sum("call_count").alias("total_calls")
    )

    sms_per_region_day = df.groupBy("region_name", "day").agg(
        sum("sms_count").alias("total_sms")
    )

    internet_daily = df.groupBy("day").agg(
        sum("internet_usage").alias("total_internet")
    )

    peak_hours = df.groupBy("hour").agg(
        sum("internet_usage").alias("usage")
    ).orderBy(col("usage").desc()).limit(5)

    return calls_per_hour, sms_per_region_day, internet_daily, peak_hours


# ✅ 7. Write Output
def write(df, summary):

    print("Writing processed data to Parquet format...")

    # ✅ Write cleaned data
    df.write \
        .mode("overwrite") \
        .partitionBy("day") \
        .parquet("data/processed/telecom_data")

    # ✅ Write aggregated outputs separately
    calls_per_hour, sms_per_region_day, internet_daily, peak_hours = summary

    calls_per_hour.write.mode("overwrite").parquet("data/processed/calls_per_hour")
    sms_per_region_day.write.mode("overwrite").parquet("data/processed/sms_per_region_day")
    internet_daily.write.mode("overwrite").parquet("data/processed/internet_daily")
    peak_hours.write.mode("overwrite").parquet("data/processed/peak_hours")

    print("✅ Data written successfully in Parquet format")

# ✅ MAIN PIPELINE
def main():

    spark = create_session()

    df = load(spark)

    df = clean(df)

    df = enrich(df, spark)

    df = optimize(df)

    summary = aggregate(df)

    write(df, summary)

    print("Pipeline executed successfully ✅ (final version)")

    spark.stop()

if __name__ == "__main__":
    main()