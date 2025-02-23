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
      navigate("/dashboard"); // ✅ Redirect to Dashboard if logged in
    } else {
      setAuthOpen(true); // ✅ Open login/signup modal if not logged in
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
        <Button variant="contained" sx={{ backgroundColor: "#ff44ff", color: "black", mr: 2 }} onClick={handleGetStarted}>
          Get Started
        </Button>
        <Button variant="outlined" sx={{ borderColor: "#ff44ff", color: "#ff44ff" }} onClick={() => navigate("/dashboard")}>
          View Dashboard
        </Button>
      </Box>
      <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} />
    </Container>
  );
};

export default LandingPage;
