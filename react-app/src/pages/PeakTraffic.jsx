import { useEffect, useState } from "react";
import API from "../api";

export default function PeakTraffic() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("/usage/peak")
      .then(res => setData(res.data))
      .catch(() => console.log("Error loading peak data"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div style={container}>
      <h2>📈 Peak Traffic</h2>

      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        
        {/* ✅ Top Hours */}
        <div style={box}>
          <h3>⏰ Top Hours</h3>
          {data.top_hours.map((h, i) => (
            <div key={i} style={card}>
              <strong>Hour {h.hour}</strong>
              <p>Usage: {h.total_usage}</p>
            </div>
          ))}
        </div>

        {/* ✅ Top Regions */}
        <div style={box}>
          <h3>🌍 Top Regions</h3>
          {data.top_regions.map((r, i) => (
            <div key={i} style={card}>
              <strong>{r.region}</strong>
              <p>Usage: {r.total_usage}</p>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

//
// ✅ ✅ STYLES
//

const container = {
  marginBottom: "30px",
  background: "#fff",
  padding: "20px",
  borderRadius: "10px",
  boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
};

const box = {
  background: "#f9f9f9",
  padding: "15px",
  borderRadius: "8px",
  minWidth: "220px",
  flex: 1
};

const card = {
  background: "#fff",
  padding: "10px",
  marginBottom: "10px",
  borderRadius: "6px",
  border: "1px solid #eee"
};