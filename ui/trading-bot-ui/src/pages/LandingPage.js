import React, { useState } from "react";
import { Container, Typography, Button, Box, Grid, Card, CardContent } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import AuthModal from "../components/auth/AuthModal";
import Footer from "../components/common/Footer";
import { motion } from "framer-motion";
import tradingGif from "../assets/algotrading-ui.gif"; // ✅ Background Image

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
        background: "linear-gradient(to right, #007bff, #00c6ff)",
      }}
    >
      {/* ✅ Background Image */}
      <Box
        component="img"
        src={tradingGif}
        alt="Algo Trading UI"
        sx={{
          position: "absolute",
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: 0.2,
          zIndex: -1,
        }}
      />

      {/* ✅ Hero Section */}
      <Container maxWidth="lg" sx={{ textAlign: "center", paddingTop: "6rem", position: "relative", zIndex: 1 }}>
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
          <Typography variant="h2" sx={{ fontWeight: "bold", color: "#ffffff" }}>
            AI-Powered Algo Trading
          </Typography>
          <Typography variant="h5" sx={{ color: "#e0e0e0", marginTop: "1rem" }}>
            This system **trades autonomously** based on provided AI strategies,  
            continuously backtests, paper trades, and optimizes real trading execution.
          </Typography>
        </motion.div>

        <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
          <Button
            variant="contained"
            sx={{
              backgroundColor: "#ffcc00",
              color: "#212529",
              marginTop: "2rem",
              padding: "14px 28px",
              fontSize: "18px",
              fontWeight: "bold",
              borderRadius: "8px",
              "&:hover": { backgroundColor: "#ffdd33" },
            }}
            onClick={handleGetStarted}
          >
            {isAuthenticated() ? "Go to Dashboard" : "Get Started"}
          </Button>
        </motion.div>
      </Container>

      {/* ✅ How AI Trading Works */}
      <Container maxWidth="md" sx={{ marginTop: "5rem", textAlign: "center" }}>
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#ffffff" }}>
          How AI Trading Works
        </Typography>
        <Typography variant="body1" sx={{ color: "#e0e0e0", marginTop: "1rem" }}>
          The AI continuously backtests strategies, runs paper trading for validation,  
          and executes live trades with optimal risk management.
        </Typography>
        <Grid container spacing={4} sx={{ marginTop: "2rem" }}>
          {[
            { icon: "📊", title: "Backtesting", text: "AI tests strategies on historical data for performance analysis." },
            { icon: "🔄", title: "Paper Trading", text: "Risk-free virtual trading to fine-tune strategies before live execution." },
            { icon: "⚡", title: "Live Execution", text: "Optimized trading decisions executed automatically in real-time." },
          ].map((feature, index) => (
            <Grid item xs={12} sm={4} key={index}>
              <motion.div whileHover={{ scale: 1.05 }}>
                <Box textAlign="center" sx={{ color: "#ffffff" }}>
                  <Typography variant="h5">{feature.icon} {feature.title}</Typography>
                  <Typography variant="body1">{feature.text}</Typography>
                </Box>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* ✅ AI Trading Strategies */}
      <Container maxWidth="lg" sx={{ marginTop: "5rem", textAlign: "center" }}>
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#ffffff" }}>
          AI Trading Strategies
        </Typography>
        <Grid container spacing={3} sx={{ marginTop: "2rem" }}>
          {[
            { name: "Mean Reversion", description: "AI identifies assets that deviate from their average price and capitalizes on their return to mean." },
            { name: "Momentum Trading", description: "AI detects trends and executes trades following market momentum." },
            { name: "Statistical Arbitrage", description: "Using advanced ML models, AI finds arbitrage opportunities in real-time." },
            { name: "High-Frequency Trading", description: "AI executes thousands of trades in milliseconds, capturing micro-price movements." },
          ].map((strategy, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card sx={{ background: "#ffffff", borderRadius: "10px", padding: "20px", boxShadow: "0px 4px 12px rgba(0,0,0,0.1)" }}>
                <CardContent>
                  <Typography variant="h5" sx={{ fontWeight: "bold", color: "#007bff" }}>
                    {strategy.name}
                  </Typography>
                  <Typography variant="body1">{strategy.description}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* ✅ Detailed Performance Monitoring */}
      <Container maxWidth="md" sx={{ marginTop: "5rem", textAlign: "center" }}>
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#ffffff" }}>
          Full Performance Tracking
        </Typography>
        <Typography variant="body1" sx={{ color: "#e0e0e0", marginTop: "1rem" }}>
          Get detailed reports of AI's decision-making process, trade execution results, and profitability metrics.
        </Typography>
        <Button
          variant="contained"
          sx={{
            backgroundColor: "#007bff",
            color: "#ffffff",
            marginTop: "2rem",
            padding: "12px 24px",
            fontSize: "16px",
            fontWeight: "bold",
            "&:hover": { backgroundColor: "#0056b3" },
          }}
        >
          View Performance Dashboard
        </Button>
      </Container>

      {/* ✅ Login Modal */}
      <AuthModal open={authOpen} handleClose={handleCloseAuthModal} />

      {/* ✅ Footer */}
      <Footer />
    </Box>
  );
};

export default LandingPage;
