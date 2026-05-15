import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  const cards = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Peak Traffic", path: "/peak" },
    { name: "Region Explorer", path: "/region" },
    { name: "Prediction", path: "/prediction" }
  ];

  return (
    <div style={container}>
      <p style={subtitle}>SELECT A MODULE TO EXPLORE</p>

      <div style={grid}>
        {cards.map((item) => (
          <div
            key={item.name}
            style={card}
            onClick={() => navigate(item.path)}
          >
            <h3 style={cardText}>{item.name}</h3>
          </div>
        ))}
      </div>
    </div>
  );
}

const container = {
  textAlign: "center",
  padding: "60px 20px",
  background: "#f5f5f5",
  minHeight: "100vh"
};

const title = {
  fontSize: "28px",
  fontWeight: "600",
  marginBottom: "10px",
  color: "#111"
};

const subtitle = {
  color: "#666",
  fontSize: "14px",
  marginBottom: "40px"
};

const grid = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
  gap: "25px",
  maxWidth: "800px",
  margin: "0 auto"
};

const card = {
  background: "#ffffff",
  padding: "30px",
  borderRadius: "12px",
  cursor: "pointer",
  border: "1px solid #e5e5e5",
  boxShadow: "0 6px 15px rgba(0,0,0,0.05)",
  transition: "all 0.25s ease",
  onMouseEnter: (e) => {
  e.currentTarget.style.transform = "translateY(-5px)";
  e.currentTarget.style.boxShadow = "0 12px 25px rgba(0,0,0,0.08)";
  },
  onMouseLeave: (e) => {
  e.currentTarget.style.transform = "translateY(0)";
  e.currentTarget.style.boxShadow = "0 6px 15px rgba(0,0,0,0.05)";
  }
};

const cardText = {
  color: "#222",
  fontWeight: "500",
};
