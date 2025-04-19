// src/components/landing/HeroSection.jsx
import { motion } from "framer-motion";
import { Box, Typography, Button, Container, Grid } from "@mui/material";
import heroImage from "../../assets/ai-illustration.png";

const HeroSection = ({ onGetStarted }) => {
  return (
    <Box sx={{ bgcolor: "#0A0B0E", py: 12 }}>
      <Container maxWidth="lg">
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, x: -40 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Typography
                variant="h2"
                sx={{ fontWeight: 700, color: "#fff", mb: 2 }}
              >
                The Future of{" "}
                <span style={{ color: "#00E5FF" }}>AI Trading</span>
              </Typography>
              <Typography variant="h6" sx={{ color: "#bbb", mb: 4 }}>
                Automate. Analyze. Outperform the Market with GrowthQuantix.
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={onGetStarted}
                sx={{
                  bgcolor: "#00E5FF",
                  color: "#000",
                  px: 4,
                  py: 1.5,
                  borderRadius: "50px",
                  fontWeight: 600,
                  "&:hover": { bgcolor: "#00B2CC" },
                }}
              >
                Get Started Free
              </Button>
            </motion.div>
          </Grid>
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, x: 40 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Box
                component="img"
                src={heroImage}
                alt="AI Bot Illustration"
                sx={{ width: "100%", maxWidth: "500px", mx: "auto" }}
              />
            </motion.div>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default HeroSection;
