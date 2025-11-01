import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";

function App() {
  return (
    <Routes>
      {/* ✅ Default route for root */}
      <Route path="/" element={<LoginPanel />} />

      {/* 🔹 Explicit login and register routes */}
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;