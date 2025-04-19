// src/pages/LandingPage.jsx

import React, { useState, lazy, Suspense } from "react";
import { Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../services/authService";
import NavBar from "../components/landing/NavBar";
import HeroSection from "../components/landing/HeroSection";
import StrategySection from "../components/landing/StrategySection";
import ToolsSection from "../components/landing/ToolsSection";
import BacktestSection from "../components/landing/BacktestSection";
import FAQSection from "../components/landing/FAQSection";
import VideoEmbedSection from "../components/landing/VideoEmbedSection";
import PricingPlansSection from "../components/landing/PricingSection";
import TrustBadgesSection from "../components/landing/TrustBadgesSection";
import ScreenerAlertsSection from "../components/landing/ScreenerAlertsSection";
import AIAgentSection from "../components/landing/AIAgentSection";
import Footer from "../components/common/Footer";
import HowAIWorksSection from "../components/landing/HowAIWorksSection";
import StrategyBacktestingSection from "../components/landing/StrategyBacktestingSection";
import ToolkitSection from "../components/landing/ToolkitSection";
import VisionSection from "../components/landing/VisionSection";
import TestimonialsSection from "../components/landing/TestimonialsSection";
import SupportedBrokersSection from "../components/landing/SupportedBrokersSection";

// Lazy load the Auth modal
const LazyAuthModal = lazy(() => import("../components/auth/AuthModal"));

const LandingPage = () => {
  const navigate = useNavigate();
  const isUserAuthenticated = isAuthenticated();
  const [authOpen, setAuthOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);

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
      {/* Custom Navbar */}
      <NavBar
        onSignIn={() => {
          setIsLogin(true);
          setAuthOpen(true);
        }}
        onSignUp={() => {
          setIsLogin(false);
          setAuthOpen(true);
        }}
      />

      {/* All Sections Combined */}
      <Box sx={{ bgcolor: "#000", color: "#fff" }}>
        <HeroSection onGetStarted={handleGetStarted} />
        <VideoEmbedSection />
        <StrategySection />
        <ToolsSection />
        <ScreenerAlertsSection />
        <HowAIWorksSection />
        <StrategyBacktestingSection />
        <AIAgentSection />
        <PricingPlansSection />
        <TrustBadgesSection />
        <BacktestSection />
        <SupportedBrokersSection />
        <ToolkitSection />
        <VisionSection />
        <TestimonialsSection />
        <FAQSection />
        <Footer />
      </Box>

      {/* Auth Modal (Sign In/Up) */}
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
    </>
  );
};

export default LandingPage;
