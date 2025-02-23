import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/common/Navbar";
import LandingPage from "./pages/LandingPage";
import DashboardPage from "./pages/DashboardPage";
import { isAuthenticated } from "./services/authService";
import ThemeProviderWrapper from "./context/ThemeContext";
import { CssBaseline } from "@mui/material";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(isAuthenticated());

  return (
    <ThemeProviderWrapper>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={isLoggedIn ? <DashboardPage /> : <Navigate to="/" />} />
        </Routes>
      </Router>
    </ThemeProviderWrapper>
  );
};

export default App;
