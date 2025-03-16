import React, { useState, lazy, Suspense } from "react";
import { Container, Typography, Button, Box, styled } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import Footer from "../components/common/Footer";
import bgImage from "../assets/trading-bg.jpg";


// Lazy Import for AuthModal
const LazyAuthModal = lazy(() => import("../components/auth/AuthModal"));

const GradientBox = styled(Box)(({ theme }) => ({
  minHeight: "100vh",
  textAlign: "center",
  background: `linear-gradient(135deg,rgba(116, 130, 135, 0.07) 30%, hsla(196, 100.00%, 46.90%, 0.85) 90%), 
               url(${bgImage})`,
  backgroundSize: "cover",
  backgroundPosition: "center 20%", // Moves the image slightly down
  backgroundRepeat: "no-repeat",
  color: "#ffffff",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  padding: theme.spacing(4),
}));



const StyledButton = styled(Button)(() => ({
  padding: "16px 32px",
  fontSize: "1.2rem",
  fontWeight: "bold",
  backgroundColor: "#00AEEF",
  color: "#ffffff",
  borderRadius: "30px",
  transition: "0.3s ease-in-out",
  "&:hover": {
    backgroundColor: "#008CBA",
    transform: "scale(1.05)",
    boxShadow: "0px 0px 18px rgba(15, 15, 14, 0.26)",
  },
}));

const Section = styled(Box)(({ theme }) => ({
  padding: theme.spacing(8, 4),
  backgroundColor: "#f9f9f9",
  textAlign: "center",
  borderBottom: "2px solidrgba(0, 175, 239, 0.6)",
}));

const LandingPage = () => {
  const navigate = useNavigate();
  const [authOpen, setAuthOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const isUserAuthenticated = isAuthenticated();

  const handleGetStarted = () => {
    if (isUserAuthenticated) {
      navigate("/dashboard");
    } else {
      setIsLogin(true);
      setAuthOpen(true);
    }
  };

  return (
    <>
      {/* Navigation */}
      <Box
        component="nav"
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bgcolor: "white",
          zIndex: 1000,
          boxShadow: 1,
          padding: "12px 0",
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Typography variant="h5" sx={{ fontWeight: "bold", color: "#00AEEF", display: "flex", alignItems: "center" }}>
              <Box component="svg" sx={{ width: 32, height: 32, mr: 1 }} viewBox="0 0 24 24">
                <path fill="#00AEEF" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z" />
              </Box>
              AI- Trading
            </Typography>
            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => {
                  setIsLogin(true);
                  setAuthOpen(true);
                }}
              >
                Sign In
              </Button>
              <Button
                variant="contained"
                sx={{ bgcolor: "grey.800", "&:hover": { bgcolor: "grey.900" } }}
                onClick={() => {
                  setIsLogin(false);
                  setAuthOpen(true);
                }}
              >
                Sign Up
              </Button>
            </Box>
          </Box>
        </Container>
      </Box>

      {/* Hero Section */}
      <GradientBox sx={{ paddingTop: "80px" }}>
        <Container maxWidth="lg">
          <Typography variant="h2" sx={{ fontWeight: "bold", letterSpacing: 1, mb: 2 }}>
            AI-Powered Trading
          </Typography>
          <Typography variant="h5" sx={{ mt: 2, opacity: 0.9, fontWeight: 300, mb: 4 }}>
            Automate trading, manage risks, and optimize performance with cutting-edge AI strategies.
          </Typography>
          <StyledButton onClick={handleGetStarted}>
            {isUserAuthenticated ? "Go to Dashboard" : "Start Trading Now"}
          </StyledButton>
        </Container>
      </GradientBox>

      {/* New Sections */}
      <Section id="about-us">
        <Typography variant="h4" sx={{ fontWeight: "bold", mb: 2 }}>About Us</Typography>
        <Typography variant="body1">Welcome to AlgoTrade AI, the future of trading powered by Artificial Intelligence. Our mission is to revolutionize the way retail traders engage with the markets by providing a fully automated trading platform that’s intelligent, efficient, and designed for long-term success.

At AlgoTrade AI, we believe that trading should be accessible, intelligent, and systematic. That’s why we’ve developed an AI-driven platform that not only automates your trades but also analyzes market trends, optimizes risk/reward ratios, and places orders with precision. Our focus is on helping you make smarter, data-driven decisions with the power of advanced technology—whether you're a seasoned trader or just starting out.

With a vision to democratize trading for all, we’re building a future where retail traders can leverage the same tools and strategies as institutional investors. Our platform is designed to reduce the complexities of trading while offering you the highest level of performance and control..</Typography>
      </Section>

      <Section id="our-strategy-backtesting">
  <Typography variant="h4" sx={{ fontWeight: "bold", mb: 2 }}>Our Strategy & Backtesting</Typography>
  
  <Typography variant="body1" sx={{ mb: 2 }}>
    At <strong>AlgoTrade AI</strong>, we don’t just rely on theory—we back our strategies with over three years of rigorous backtesting and real-market performance. Our approach is built on a foundation of data-driven insights and continuous refinement, ensuring that every trade is backed by proven, real-world results.
  </Typography>

  <Typography variant="h5" sx={{ fontWeight: "bold", mt: 3, mb: 1 }}>Powerful, Time-Tested Strategies</Typography>
  <Typography variant="body1" sx={{ mb: 2 }}>
    Our AI-powered strategies are the product of over three years of intense market analysis, testing, and optimization. We've fine-tuned our models across various market conditions, guaranteeing consistent and reliable results—whether you're engaging in high-frequency trading (HFT) or long-term investment strategies.
  </Typography>

  <Typography variant="h5" sx={{ fontWeight: "bold", mt: 3, mb: 1 }}>Advanced Backtesting Engine</Typography>
  <Typography variant="body1" sx={{ mb: 2 }}>
    With our state-of-the-art backtesting framework, we simulate real-world trading scenarios with exceptional accuracy. By factoring in everything from slippage to market volatility, our system ensures that our strategies are not only theoretical but ready to thrive in dynamic market environments.
  </Typography>

  <Typography variant="h5" sx={{ fontWeight: "bold", mt: 3, mb: 1 }}>Evolving for Excellence</Typography>
  <Typography variant="body1" sx={{ mb: 2 }}>
    At <strong>AlgoTrade AI</strong>, we don’t settle for yesterday's performance. Our algorithms continuously learn from each trade, adapting to the market and refining strategies in real time to stay ahead of the curve and maximize profitability.
  </Typography>

  <Typography variant="body1">
    With <strong>AlgoTrade AI</strong>, you’re not just trading—you’re leveraging a system that’s been rigorously tested, proven, and optimized for success, ensuring you get the edge in any market condition.
  </Typography>
</Section>


      <Section id="our-vision">
  <Typography variant="h4" sx={{ fontWeight: "bold", mb: 2 }}>Our Vision</Typography>
  
  <Typography variant="body1" sx={{ mb: 2 }}>
    At <strong>AlgoTrade AI</strong>, our vision is to empower retail traders worldwide by providing them with cutting-edge, AI-driven trading solutions that level the playing field in financial markets.  
  </Typography>

  <Typography variant="body1" sx={{ mb: 2 }}>
    We aim to create a future where every trader—regardless of experience—can harness the full potential of automation, advanced analytics, and intelligent risk management to make smarter, data-backed decisions.
  </Typography>

  <Typography variant="body1" sx={{ mb: 2 }}>
    We believe that the future of trading lies in the seamless integration of artificial intelligence and human strategy. By offering retail traders the same advanced tools and insights that were once reserved for institutional investors, we are not just shaping the future of trading; we are shaping the future of financial independence for all.
  </Typography>

  <Typography variant="body1">
    Our long-term vision is to continually innovate, ensuring that <strong>AlgoTrade AI</strong> remains at the forefront of automated trading technology, creating opportunities for growth, profitability, and success in the dynamic world of finance.
  </Typography>
</Section>


      <Section id="why-choose-us">
  <Typography variant="h4" sx={{ fontWeight: "bold", mb: 2 }}>Why Choose Us?</Typography>
  
  <Typography variant="body1" sx={{ fontWeight: "bold", mt: 2 }}>AI-Powered Insights:</Typography>
  <Typography variant="body1" sx={{ mb: 2 }}>
    Our machine learning models analyze market trends and optimize your trades in real-time, ensuring you make the most informed decisions.
  </Typography>

  <Typography variant="body1" sx={{ fontWeight: "bold" }}>Automated Trading:</Typography>
  <Typography variant="body1" sx={{ mb: 2 }}>
    Sit back and let the AI handle your trades with intelligent risk management, order execution, and strategy optimization—all in real-time.
  </Typography>

  <Typography variant="body1" sx={{ fontWeight: "bold" }}>Risk Management:</Typography>
  <Typography variant="body1" sx={{ mb: 2 }}>
    We prioritize your safety with built-in risk/reward analysis, ensuring that every trade is optimized for maximum profitability with minimized risk.
  </Typography>

  <Typography variant="body1" sx={{ fontWeight: "bold" }}>High-Speed Execution:</Typography>
  <Typography variant="body1" sx={{ mb: 2 }}>
    Our platform supports high-frequency trading (HFT) to ensure low-latency execution and quick responses to market changes.
  </Typography>

  <Typography variant="body1" sx={{ fontWeight: "bold" }}>For Retail Traders:</Typography>
  <Typography variant="body1">
    We’re here to level the playing field and provide retail traders with the tools needed to compete with institutional investors.
  </Typography>
  <Typography variant="body1" sx={{ fontWeight: "bold" }}>For Retail Traders:</Typography>
        <Typography variant="body1">
          We're here to level the playing field and provide retail traders with the tools needed to compete with institutional investors.
        </Typography>
</Section>


    

      {/* Ensure AuthModal works correctly */}
      <Suspense fallback={<Box>Loading...</Box>}>
        {authOpen && (
          <LazyAuthModal
            open={authOpen}
            handleClose={() => setAuthOpen(false)}
            onLoginSuccess={() => {
              setAuthOpen(false);
              navigate("/dashboard");
            }}
            isLogin={isLogin}
            setIsLogin={setIsLogin}
          />
        )}
      </Suspense>

      {/* Correct Footer Placement */}
      <Box sx={{ bgcolor: "#001F3F", color: "white", mt: 4, py: 3 }}>
        <Footer />
      </Box>
    </>
  )
};

export default LandingPage;