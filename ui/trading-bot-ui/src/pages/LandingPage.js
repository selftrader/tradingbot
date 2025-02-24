import React, { useState } from "react";
import { Container, Typography, Button, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import AuthModal from "../components/auth/AuthModal";

const LandingPage = () => {
  const navigate = useNavigate();
  const [authOpen, setAuthOpen] = useState(false);

  const handleGetStarted = () => {
    if (isAuthenticated()) {
      navigate("/dashboard");  // ✅ Redirect to Dashboard if logged in
    } else {
      setAuthOpen(true);  // ✅ Open login modal if not logged in
    }
  };

  const handleViewDashboard = () => {
    if (isAuthenticated()) {
      navigate("/dashboard");  // ✅ If logged in, go to Dashboard
    } else {
      setAuthOpen(true);  // ✅ If not logged in, open login modal
    }
  };

  return (
    <Container sx={{ textAlign: "center", mt: 10 }}>
      <Typography variant="h3" sx={{ fontWeight: "bold", color: "#ff44ff" }}>
        Welcome to Trading Bot AI
      </Typography>
      <Typography variant="h6" sx={{ mt: 2, color: "white" }}>
        The best AI-powered trading platform for Indian markets (NSE/BSE).
      </Typography>
      <Box sx={{ mt: 4 }}>
        {/* ✅ "Get Started" now works correctly */}
        <Button variant="contained" sx={{ backgroundColor: "#ff44ff", color: "black", mr: 2 }} onClick={handleGetStarted}>
          Get Started
        </Button>

        {/* ✅ "View Dashboard" now opens login modal when logged out */}
        <Button variant="outlined" sx={{ borderColor: "#ff44ff", color: "#ff44ff" }} onClick={handleViewDashboard}>
          View Dashboard
        </Button>
      </Box>

      {/* ✅ Login Modal */}
      <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} />
    </Container>
  );
};

export default LandingPage;
