import React, { useState } from "react";
import { Container, Typography, Button, Box, Link, Grid, useTheme, Card, CardContent } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import Footer from "../components/common/Footer";
import AuthModal from "../components/auth/AuthModal";

const LandingPage = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const [authOpen, setAuthOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);

  const handleGetStarted = () => {
    if (isAuthenticated()) {
      navigate("/dashboard");
    } else {
      setIsLogin(true);
      setAuthOpen(true);
    }
  };

  const handleSignupOpen = () => {
    setIsLogin(false);
    setAuthOpen(true);
  };

  const handleLoginSuccess = () => {
    setAuthOpen(false);
    navigate("/dashboard");
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        textAlign: "center",
        backgroundColor: theme.palette.background.default,
        color: theme.palette.text.primary,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: { xs: 2, md: 6 },
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="h2" sx={{ fontWeight: "bold", letterSpacing: 1, mb: 2, color: theme.palette.primary.main }}>
          AI-Powered Algo Trading
        </Typography>
        <Typography variant="h5" sx={{ mt: 2, opacity: 0.9, fontWeight: 300, color: theme.palette.text.secondary }}>
          Automate trading, manage risks, and optimize performance with cutting-edge AI strategies.
        </Typography>
        <Grid container spacing={4} sx={{ mt: 5, justifyContent: "center" }}>
          {[{
            title: "AI-Driven Market Analysis",
            description: "Leverage real-time AI analytics to make data-driven trading decisions."
          }, {
            title: "High-Speed Execution",
            description: "Execute trades instantly with our ultra-low latency trading engine."
          }, {
            title: "Risk Management Tools",
            description: "Automated risk controls to protect your investments."
          }, {
            title: "Customizable Trading Strategies",
            description: "Define and test your own strategies with advanced backtesting features."
          }].map((feature, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card sx={{ backgroundColor: theme.palette.background.paper, boxShadow: 4, padding: 2 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: "bold" }}>{feature.title}</Typography>
                  <Typography variant="body2" color="text.secondary">{feature.description}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
        <Box sx={{ display: "flex", justifyContent: "center", mt: 5 }}>
          <Button
            variant="contained"
            sx={{ padding: "16px 32px", fontSize: "1.2rem", fontWeight: "bold", backgroundColor: theme.palette.primary.main, color: "#ffffff" }}
            onClick={handleGetStarted}
          >
            {isAuthenticated() ? "Go to Dashboard" : "Start Trading Now"}
          </Button>
        </Box>
        <Typography variant="body1" sx={{ mt: 4 }}>
          New to AI Trading?{" "}
          <Link onClick={handleSignupOpen} sx={{ cursor: "pointer", color: theme.palette.secondary.main, fontWeight: "bold" }}>
            Create an Account
          </Link>
        </Typography>
      </Container>
      {authOpen && (
        <AuthModal
          open={authOpen}
          handleClose={() => setAuthOpen(false)}
          onLoginSuccess={handleLoginSuccess} // ✅ Fix: Added missing function
          isLogin={isLogin}
          setIsLogin={setIsLogin}
        />
      )}
      <Footer />
    </Box>
  );
};

export default LandingPage;
