import { useState } from "react";
import API from "../api";

export default function Prediction() {
  const [form, setForm] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = () => {
    setLoading(true);

    API.post("/predict-usage-risk", form)
      .then(res => setResult(res.data))
      .catch(() => alert("Prediction failed"))
      .finally(() => setLoading(false));
  };

  return (
    <div style={container}>
      <h2 style={title}>⚠️ Risk Prediction</h2>

      <div style={mainBox}>
        
        {/* ✅ Left Form */}
        <div style={formBox}>

          <label style={label}>Region</label>
          <input
            style={input}
            placeholder="e.g. Region_A"
            onChange={(e) =>
              setForm({ ...form, region: e.target.value })
            }
          />

          <label style={label}>Average Usage</label>
          <input
            style={input}
            type="number"
            placeholder="e.g. 1500"
            onChange={(e) =>
              setForm({ ...form, avg_usage: Number(e.target.value) })
            }
          />

          <label style={label}>Growth Rate</label>
          <input
            style={input}
            type="number"
            placeholder="e.g. 0.2"
            onChange={(e) =>
              setForm({ ...form, growth_rate: Number(e.target.value) })
            }
          />

          <label style={label}>Variability</label>
          <input
            style={input}
            type="number"
            placeholder="e.g. 300"
            onChange={(e) =>
              setForm({ ...form, variability: Number(e.target.value) })
            }
          />

          <button style={button} onClick={submit}>
            {loading ? "Predicting..." : "Predict"}
          </button>

        </div>

        {/* ✅ Right Result */}
        <div style={resultContainer}>

          {!result && (
            <p style={placeholder}>Prediction result will appear here</p>
          )}

          {result && (
            <div style={resultBox(result.congestion_risk)}>

              <h3 style={{ marginBottom: "10px" }}>Prediction Result</h3>

              <div style={badge(result.congestion_risk)}>
                {result.congestion_risk}
              </div>

              <p><b>Anomaly:</b> {result.anomaly_flag.toString()}</p>
              <p><b>Score:</b> {result.score.toFixed(2)}</p>

            </div>
          )}

        </div>

      </div>
    </div>
  );
}

////////////////////////////////////////////////////////////
// ✅ STYLES (PROFESSIONAL UI)
////////////////////////////////////////////////////////////

const container = {
  padding: "20px"
};

const title = {
  marginBottom: "20px"
};

const mainBox = {
  display: "flex",
  gap: "40px",
  flexWrap: "wrap"
};

const formBox = {
  background: "#fff",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 6px 15px rgba(0,0,0,0.06)",
  width: "260px",
  display: "flex",
  flexDirection: "column",
  gap: "10px"
};

const label = {
  fontSize: "13px",
  color: "#666"
};

const input = {
  padding: "10px",
  borderRadius: "6px",
  border: "1px solid #ddd",
  outline: "none"
};

const button = {
  marginTop: "10px",
  padding: "10px",
  background: "#111",
  color: "#fff",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
};

const resultContainer = {
  flex: 1,
  minWidth: "250px",
  display: "flex",
  alignItems: "center"
};

const placeholder = {
  color: "#999"
};

const resultBox = (risk) => {
  let color = "#999";
  if (risk === "HIGH") color = "#ff4d4f";
  else if (risk === "MEDIUM") color = "#faad14";
  else if (risk === "LOW") color = "#52c41a";

  return {
    background: "#fff",
    padding: "25px",
    borderRadius: "12px",
    borderLeft: `6px solid ${color}`,
    boxShadow: "0 4px 10px rgba(0,0,0,0.08)"
  };
};

const badge = (risk) => {
  let bg = "#ddd";
  let color = "#333";

  if (risk === "HIGH") {
    bg = "#ffe5e5";
    color = "#d00000";
  } else if (risk === "MEDIUM") {
    bg = "#fff3d9";
    color = "#b36b00";
  } else if (risk === "LOW") {
    bg = "#e8f8ea";
    color = "#2e7d32";
  }

  return {
    display: "inline-block",
    padding: "6px 12px",
    borderRadius: "6px",
    fontWeight: "600",
    marginBottom: "10px",
    background: bg,
    color: color
  };
};
