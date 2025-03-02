import React, { useState } from "react";
import { Container, Typography, Button, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import AuthModal from "../components/auth/AuthModal";
import Footer from "../components/common/Footer";

const LandingPage = () => {
  const navigate = useNavigate();
  const [authOpen, setAuthOpen] = useState(false);

  const handleGetStarted = () => {
    if (isAuthenticated()) {
      navigate("/dashboard");
    } else {
      setAuthOpen(true);
    }
  };

  return (
    <Box sx={{ 
      minHeight: "100vh", 
      textAlign: "center", 
      background: "linear-gradient(to right, #1E3A8A, #22D3EE)", 
      color: "#ffffff",
      display: "flex", 
      flexDirection: "column", 
      justifyContent: "center",
      padding: { xs: 2, md: 5 }
    }}>
      <Container>
        <Typography variant="h2" sx={{ fontWeight: "bold" }}>
          AI-Powered Algo Trading
        </Typography>
        <Typography variant="h5" sx={{ mt: 2 }}>
          Trade smarter with AI-driven strategies that execute automatically.
        </Typography>
        <Button variant="contained" sx={{ mt: 3, padding: "14px 28px" }} onClick={handleGetStarted}>
          {isAuthenticated() ? "Go to Dashboard" : "Get Started"}
        </Button>
      </Container>
      <AuthModal open={authOpen} handleClose={() => setAuthOpen(false)} />
    </Box>
    
  );
};

export default LandingPage;
