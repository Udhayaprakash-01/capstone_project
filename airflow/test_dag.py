# ✅ Import your DAG functions
from dags.telecom_dag import (
    detect_files,
    validate_files,
    move_files,
    run_spark_job,
    notify
)

# ✅ Simulate Airflow context
class MockTI:
    def __init__(self):
        self.store = {}

    def xcom_push(self, key, value):
        self.store[key] = value

    def xcom_pull(self, task_ids):
        return self.store.get(task_ids)


mock_ti = MockTI()


def test_pipeline():

    print("Testing detect_files...")
    files = detect_files()
    mock_ti.xcom_push("detect_files", files)

    print("\nTesting validate_files...")
    result = validate_files(ti=mock_ti)
    mock_ti.xcom_push("validate_files", result)

    print("\nTesting move_files...")
    move_files(ti=mock_ti)

    print("\nTesting Spark job...")
    run_spark_job()

    print("\nTesting notify...")
    notify()

    print("\n✅ DAG test completed!")


if __name__ == "__main__":
    test_pipeline()
