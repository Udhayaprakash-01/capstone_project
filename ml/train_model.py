from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pandas as pd
from sqlalchemy import create_engine

# ✅ DB connection
engine = create_engine("mysql+pymysql://root:root@localhost/telecom_db")

# ✅ Load RAW DATA (IMPORTANT ✅)
df = pd.read_sql("SELECT * FROM fact_usage", engine)

# ✅ Feature engineering (row-level ✅)
df["avg_usage"] = df["internet_mb"]
df["growth_rate"] = 0.1
df["variability"] = df["internet_mb"]
df["peak_ratio"] = df["internet_mb"] / df["internet_mb"].mean()

# ✅ Label creation
threshold_high = df["avg_usage"].quantile(0.9)
threshold_med = df["avg_usage"].quantile(0.7)

def label(row):
    if row["avg_usage"] > threshold_high:
        return 2
    elif row["avg_usage"] > threshold_med:
        return 1
    else:
        return 0

df["label"] = df.apply(label, axis=1)

# ✅ Features
X = df[["avg_usage", "growth_rate", "variability", "peak_ratio"]]
y = df["label"]

# ✅ Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ✅ Model
model = RandomForestClassifier(
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# ✅ Predict
y_pred = model.predict(X_test)

# ✅ Evaluate
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))

# ✅ Save
joblib.dump(model, "ml/model.pkl")

print("✅ Model saved successfully!")