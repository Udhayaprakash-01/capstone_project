import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import RegionExplorer from "./pages/RegionExplorer";
import PeakTraffic from "./pages/PeakTraffic";
import Prediction from "./pages/Prediction";

function Layout() {
  const navigate = useNavigate();
  const location = useLocation();

  const menu = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Peak Traffic", path: "/peak" },
    { name: "Region Explorer", path: "/region" },
    { name: "Prediction", path: "/prediction" }
  ];

  return (
    <div style={container}>

      <div style={layout}>

        {/* ✅ SIDEBAR */}
        <div style={sidebar}>

          {/* ✅ TITLE INSIDE SIDEBAR */}
          <div style={sidebarTitle}>
            📡 TELECOM INTELLIGENCE
          </div>

          {menu.map((item) => (
            <div
              key={item.name}
              onClick={() => navigate(item.path)}
              style={{
                ...menuItem,
                ...(location.pathname === item.path ? activeItem : {})
              }}
            >
              {item.name}
            </div>
          ))}

        </div>

        {/* ✅ MAIN CONTENT */}
        <div style={content}>
          <Routes>
            <Route path="/" element={<Empty />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/region" element={<RegionExplorer />} />
            <Route path="/peak" element={<PeakTraffic />} />
            <Route path="/prediction" element={<Prediction />} />
          </Routes>
        </div>

      </div>
    </div>
  );
}

function Empty() {
  return (
    <div style={empty}>
      <h3>Select a module from left 👈</h3>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Layout />
    </Router>
  );
}

////////////////////////////////////////////////////////////
// ✅ STYLES (PROFESSIONAL MONOCHROME)
////////////////////////////////////////////////////////////

const container = {
  fontFamily: "'Inter', sans-serif",
};

const layout = {
  display: "flex",
  height: "100vh"
};

const sidebar = {
  width: "260px",
  background: "#111",
  color: "#fff",
  padding: "25px 20px",
  display: "flex",
  flexDirection: "column",
  gap: "12px"
};

const sidebarTitle = {
  fontSize: "14px",
  fontWeight: "600",
  letterSpacing: "1px",
  marginBottom: "15px",
  borderBottom: "1px solid #333",
  paddingBottom: "10px"
};

const menuItem = {
  cursor: "pointer",
  padding: "10px 12px",
  borderRadius: "6px",
  color: "#ccc",
  fontSize: "14px",
  transition: "all 0.2s ease"
};

const activeItem = {
  background: "#fff",
  color: "#111",
  fontWeight: "500"
};

const content = {
  flex: 1,
  padding: "25px",
  background: "#f8f9fa",
  overflowY: "auto"
};

const empty = {
  textAlign: "center",
  marginTop: "120px",
  color: "#666"
};