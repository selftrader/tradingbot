// src/components/landing/ScreenerAlertsSection.jsx
import { Box, Typography, Container, Grid } from "@mui/material";
import { motion } from "framer-motion";
import alertIcon from "../../assets/icons/alert.svg";
import screenerIcon from "../../assets/icons/screener.svg";

const ScreenerAlertsSection = () => {
  return (
    <Box sx={{ py: 10, bgcolor: "#0A0C10" }}>
      <Container maxWidth="lg">
        <Typography
          variant="h4"
          sx={{ color: "#00E5FF", fontWeight: 700, textAlign: "center", mb: 6 }}
        >
          Live Screener + Alerts
        </Typography>

        <Grid container spacing={4}>
          {[alertIcon, screenerIcon].map((icon, idx) => (
            <Grid item xs={12} md={6} key={idx}>
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.3 }}
              >
                <Box
                  sx={{
                    backgroundColor: "#14181f",
                    p: 4,
                    borderRadius: 3,
                    border: "1px solid #2f3640",
                    color: "#fff",
                    textAlign: "center",
                  }}
                >
                  <img
                    src={icon}
                    style={{ height: 60, marginBottom: 16 }}
                    alt="feature"
                  />
                  <Typography
                    variant="h6"
                    sx={{ color: "#00E5FF", fontWeight: 600 }}
                  >
                    {idx === 0 ? "Custom Alerts" : "Live Screener"}
                  </Typography>
                  <Typography sx={{ mt: 1, color: "#ccc", fontSize: 14 }}>
                    {idx === 0
                      ? "Get notified instantly when a strategy triggers"
                      : "Filter stocks in real-time based on AI signals"}
                  </Typography>
                </Box>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default ScreenerAlertsSection;
