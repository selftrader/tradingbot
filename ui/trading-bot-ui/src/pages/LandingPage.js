import React, { useState } from "react";
import { Container, Typography, Button, Box, Link } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import Footer from "../components/common/Footer";
import AuthModal from "../components/auth/AuthModal";

const LandingPage = () => {
  const navigate = useNavigate();
  const [authOpen, setAuthOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);  // ✅ Control login/signup state

  const handleGetStarted = () => {
    if (isAuthenticated()) {
      navigate("/dashboard");  // ✅ Redirect if already logged in
    } else {
      setIsLogin(true);  // ✅ Open login modal
      setAuthOpen(true);
    }
  };

  const handleSignupOpen = () => {
    setIsLogin(false);  // ✅ Open Signup modal instead of Login
    setAuthOpen(true);
  };

  const handleLoginSuccess = () => {
    setAuthOpen(false);  // ✅ Close modal after login
    navigate("/dashboard");  // ✅ Redirect to dashboard
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

        {/* ✅ Add "Need an account?" link to open signup */}
        <Typography variant="body1" sx={{ mt: 3 }}>
          Need an account?{" "}
          <Link onClick={handleSignupOpen} sx={{ cursor: "pointer", color: "#FFC107" }}>
            Sign up here
          </Link>
        </Typography>
      </Container>

      {/* ✅ Render AuthModal **only** when authOpen is true */}
      {authOpen && (
        <AuthModal
          open={authOpen}
          handleClose={() => setAuthOpen(false)}
          onLoginSuccess={handleLoginSuccess}
          isLogin={isLogin}
          setIsLogin={setIsLogin}
        />
      )}

      <Footer />
    </Box>
  );
};

export default LandingPage;
