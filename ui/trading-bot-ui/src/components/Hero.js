import { Typography, Button, Box } from "@mui/material";
import { motion } from "framer-motion";

const HeroSection = () => {
  return (
    <Box
      sx={{
        height: "90vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        backgroundImage: "url('/assets/background.png')",
        backgroundSize: "cover",
      }}
    >
      <Typography
        variant="h2"
        sx={{
          fontWeight: "bold",
          background: "linear-gradient(to right, #ff00ff, #8a2be2)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        AI-Powered Trading Bot.
      </Typography>
      <Typography
        variant="h5"
        sx={{ color: "#fff", mt: 2, opacity: 0.8 }}
      >
        Execute trades with precision and speed.
      </Typography>
      <Box sx={{ mt: 4, display: "flex", gap: 2 }}>
        <Button variant="outlined" sx={{ borderColor: "#ff00ff", color: "#ff00ff" }}>
          Get Started
        </Button>
        <Button variant="outlined" sx={{ borderColor: "#8a2be2", color: "#8a2be2" }}>
          Explore
        </Button>
      </Box>
      <motion.img
        src="/assets/robot.svg"
        style={{ width: "400px", marginTop: "50px" }}
        animate={{ scale: [0.9, 1, 0.9] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
    </Box>
  );
};

export default HeroSection;
