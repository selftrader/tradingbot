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
        {isLoggedIn && <Layout />}  {/* ✅ Navbar only shown after login */}
        <Routes>
        <Route path="/" element={!isAuthenticated() ? <LandingPage /> : <Navigate to="/dashboard" />} />
          <Route path="/login" element={isLoggedIn ? <Navigate to="/dashboard" /> : <LoginPage />} />
          <Route path="/signup" element={isLoggedIn ? <Navigate to="/dashboard" /> : <SignupPage />} />
          {/* ✅ Protect dashboard and other pages */}
          <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
          <Route path="/trade-control" element={<PrivateRoute><TradeControlPage /></PrivateRoute>} />
          <Route path="/config" element={<PrivateRoute><ConfigPage /></PrivateRoute>} />
          <Route path="/analysis" element={<PrivateRoute><StockAnalysisPage /></PrivateRoute>} />
          <Route path="/profile" element={<Navigate to="/" />} />

        </Routes>
      </Router>
    </ThemeProviderWrapper>
  );
};

export default App;
