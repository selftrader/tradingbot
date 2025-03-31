import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/common/Layout";
import LandingPage from "./pages/LandingPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import TradeControlPage from "./pages/TradeControlPage";
import ConfigPage from "./pages/BrokerConfigPage";
import { isAuthenticated } from "./services/authService";
import ThemeProviderWrapper from "./context/ThemeContext";
import { CssBaseline } from "@mui/material";
import PrivateRoute from "./routes/PrivateRoute";
import StockAnalysisPage from "./pages/StockAnalysisPage";
import ProfilePage from "./pages/ProfilePage";
import BacktestingPage from "./pages/BacktestingPage";

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

          {/* ✅ Apply Layout Globally for Private Routes */}
          <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/trade-control" element={<TradeControlPage />} />
            <Route path="/config" element={<ConfigPage />} />
            <Route path="/backtesting" element={<BacktestingPage />} /> {/* ✅ New Route */}
            <Route path="/analysis" element={<StockAnalysisPage />} />
            <Route path="/profile" element={<ProfilePage />} /> {/* ✅ Added Profile Page */}
          </Route>

          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
        </Routes>
      </Router>
    </ThemeProviderWrapper>
  );
};

export default App;
