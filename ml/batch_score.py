from feature_engineering import build_features
from predict import predict_usage_risk

df = build_features()

results = []

for _, row in df.iterrows():
    result = predict_usage_risk(row)
    result["region"] = row["region"]
    results.append(result)

import pandas as pd
pd.DataFrame(results).to_csv("ml/batch_predictions.csv", index=False)

print("✅ Batch predictions saved!")