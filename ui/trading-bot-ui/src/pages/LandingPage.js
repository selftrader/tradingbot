import React, { useState } from "react";
import { Container, Typography, Button, Box, Grid } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import AuthModal from "../components/auth/AuthModal";
import RealTimeMarket from "../components/RealTimeMarket";
import Footer from "../components/common/Footer";
import { motion } from "framer-motion";
import tradingGif from "../assets/algotrading-ui.gif";  // ✅ Background GIF

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

  const handleCloseAuthModal = () => {
    setAuthOpen(false);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        position: "relative",
        overflow: "hidden",
        color: "text.primary",
      }}
    >
      {/* ✅ Background GIF */}
      <Box
        component="img"
        src={tradingGif}
        alt="Algo Trading UI"
        sx={{
          position: "absolute",
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: 0.3, // ✅ Ensures readability
          zIndex: -1, // ✅ Places the image behind content
        }}
      />

      {/* ✅ Hero Section with Animation */}
      <Container maxWidth="lg" sx={{ textAlign: "center", paddingTop: "6rem", position: "relative", zIndex: 1 }}>
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
          <Typography variant="h3" sx={{ fontWeight: "bold", color: "primary.main" }}>
            AI-Powered Algo Trading Bot
          </Typography>
          <Typography variant="h6" sx={{ color: "text.secondary", marginTop: "1rem" }}>
            Automate your trades with AI-driven strategies. Analyze, predict, and execute trades effortlessly.
          </Typography>
        </motion.div>

        <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
          <Button
            variant="contained"
            sx={{ backgroundColor: "secondary.main", color: "text.primary", marginTop: "2rem", padding: "12px 24px", borderRadius: "8px" }}
            onClick={handleGetStarted}
          >
            {isAuthenticated() ? "Go to Dashboard" : "Get Started"}
          </Button>
        </motion.div>
      </Container>

      {/* ✅ Live Market Data Section */}
      <RealTimeMarket />

      {/* ✅ Features Section with Animations */}
      <Container maxWidth="md" sx={{ marginTop: "4rem", position: "relative", zIndex: 1 }}>
        <Grid container spacing={4}>
          {[
            { icon: "📊", title: "AI Strategy", text: "Trade with machine learning-powered strategies." },
            { icon: "⚡", title: "Real-Time Execution", text: "Lightning-fast trade execution with real-time market updates." },
            { icon: "🔒", title: "Secure & Reliable", text: "Your trading data is encrypted and securely managed." }
          ].map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Box textAlign="center">
                  <Typography variant="h5" sx={{ fontWeight: "bold", color: "primary.main" }}>{feature.icon} {feature.title}</Typography>
                  <Typography variant="body1" sx={{ color: "text.secondary" }}>{feature.text}</Typography>
                </Box>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* ✅ Login Modal */}
      <AuthModal open={authOpen} handleClose={handleCloseAuthModal} />

      {/* ✅ Common Footer Section */}
      <Footer />
    </Box>
  );
};

export default LandingPage;
