import { useEffect, useState } from "react";
import API from "../api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    API.get("/usage/summary")
      .then(res => setData(res.data))
      .catch(() => console.log("Error"));
  }, []);

  if (!data) return <p style={{ textAlign: "center" }}>Loading...</p>;

  // ✅ Chart data
  const chartData = [
    { name: "Calls", value: data.total_calls },
    { name: "SMS", value: data.total_sms },
    { name: "Internet", value: data.total_internet_mb }
  ];

  return (
    <div style={container}>
      <h2>📊 Usage Dashboard</h2>

      {/* ✅ Cards */}
      <div style={cardContainer}>
        <div style={card}>
          <h3>Calls</h3>
          <p>{data.total_calls.toLocaleString()}</p>
        </div>

        <div style={card}>
          <h3>SMS</h3>
          <p>{data.total_sms.toLocaleString()}</p>
        </div>

        <div style={card}>
          <h3>Internet</h3>
          <p>{data.total_internet_mb.toFixed(2)}</p>
        </div>
      </div>

      {/* ✅ Chart */}
      <div style={{ width: "100%", height: 300, marginTop: "30px" }}>
        <ResponsiveContainer>
          <BarChart data={chartData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#4f6df5" radius={[5, 5, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

const container = {
  textAlign: "center",
  padding: "20px"
};

const cardContainer = {
  display: "flex",
  justifyContent: "center",
  gap: "20px",
  flexWrap: "wrap",
  marginTop: "20px"
};

const card = {
  background: "white",
  padding: "20px",
  borderRadius: "10px",
  boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
  width: "200px",
  textAlign: "center"
};
