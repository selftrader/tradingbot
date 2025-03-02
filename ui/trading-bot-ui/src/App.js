import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/common/Layout";
import LandingPage from "./pages/LandingPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import TradeControlPage from "./pages/TradeControlPage";
import ConfigPage from "./pages/ConfigPage";
import { isAuthenticated } from "./services/authService";
import ThemeProviderWrapper from "./context/ThemeContext";
import { CssBaseline } from "@mui/material";
import PrivateRoute from "./routes/PrivateRoute";
import StockAnalysisPage from "./pages/StockAnalysisPage";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(isAuthenticated());

  useEffect(() => {
    const checkAuth = () => setIsLoggedIn(isAuthenticated());
    window.addEventListener("storage", checkAuth);
    return () => window.removeEventListener("storage", checkAuth);
  }, []);

  return (
    <ThemeProviderWrapper>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={isLoggedIn ? <Navigate to="/dashboard" /> : <LandingPage />} />
          <Route path="/dashboard" element={<PrivateRoute><Layout><DashboardPage /></Layout></PrivateRoute>} />
          <Route path="/trade-control" element={<PrivateRoute><Layout><TradeControlPage /></Layout></PrivateRoute>} />
          <Route path="/config" element={<PrivateRoute><Layout><ConfigPage /></Layout></PrivateRoute>} />
          <Route path="/analysis" element={<PrivateRoute><Layout><StockAnalysisPage /></Layout></PrivateRoute>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
        </Routes>
      </Router>
    </ThemeProviderWrapper>
  );
};

export default App;
