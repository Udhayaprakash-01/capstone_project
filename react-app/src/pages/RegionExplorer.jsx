import { useState } from "react";
import API from "../api";

export default function RegionExplorer() {
  const [region, setRegion] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    if (!region) return;

    setLoading(true);

    API.get(`/usage/region/${region}`)
      .then(res => setData(res.data.hourly_distribution))
      .catch(() => {
        alert("Region not found");
        setData([]);
      })
      .finally(() => setLoading(false));
  };

  return (
    <div style={container}>
      <h2 style={title}>🌍 Region Explorer</h2>

      {/* ✅ Search Box */}
      <div style={searchBox}>
        <input
          style={input}
          placeholder="Enter region (e.g. Region_A)"
          onChange={(e) => setRegion(e.target.value)}
        />
        <button style={button} onClick={fetchData}>
          Search
        </button>
      </div>

      {/* ✅ Loading */}
      {loading && <p style={loadingText}>Loading...</p>}

      {/* ✅ Results */}
      <div style={grid}>
        {data.map((item, i) => (
          <div key={i} style={card}>
            <h3 style={{ marginBottom: "10px" }}>Hour {item.hour}</h3>

            <p><b>Calls:</b> {item.call_count.toLocaleString()}</p>
            <p><b>SMS:</b> {item.sms_count.toLocaleString()}</p>
            <p><b>Internet:</b> {item.internet_mb.toFixed(2)}</p>
          </div>
        ))}
      </div>

      {/* ✅ Empty State */}
      {!loading && data.length === 0 && (
        <p style={empty}>No data found</p>
      )}
    </div>
  );
}

////////////////////////////////////////////////////////////
// ✅ PROFESSIONAL STYLES
////////////////////////////////////////////////////////////

const container = {
  padding: "20px"
};

const title = {
  marginBottom: "20px"
};

/* ✅ Search Section */
const searchBox = {
  display: "flex",
  gap: "10px",
  marginBottom: "25px"
};

const input = {
  padding: "10px",
  borderRadius: "6px",
  border: "1px solid #ddd",
  flex: 1,
  outline: "none"
};

const button = {
  padding: "10px 15px",
  background: "#111",
  color: "#fff",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
};

const loadingText = {
  color: "#666",
  marginBottom: "20px"
};

/* ✅ Grid Layout */
const grid = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
  gap: "20px"
};

/* ✅ Card Design */
const card = {
  background: "#fff",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 6px 15px rgba(0,0,0,0.06)",
  border: "1px solid #e5e5e5"
};

/* ✅ Empty State */
const empty = {
  marginTop: "20px",
  color: "#999",
  textAlign: "center"
};