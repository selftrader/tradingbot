import React from "react";
import {
  Box,
  Typography,
  Grid,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import { motion } from "framer-motion";

const VideoEmbedSection = () => {
  return (
    <Box
      sx={{
        bgcolor: "#0B1120",
        py: 10,
        px: 2,
        color: "#fff",
      }}
    >
      <Grid
        container
        spacing={4}
        alignItems="center"
        justifyContent="center"
        maxWidth="lg"
        mx="auto"
      >
        {/* Left: Video or Chart Placeholder */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Box
              sx={{
                width: "100%",
                height: "320px",
                borderRadius: "12px",
                overflow: "hidden",
                boxShadow: 3,
                background: "linear-gradient(135deg, #222, #1a1a1a)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "1.2rem",
                fontWeight: 500,
                color: "#ccc",
              }}
            >
              {/* Replace below with real <iframe> or chart image */}
              Video / Chart Preview Here
            </Box>
          </motion.div>
        </Grid>

        {/* Right: Text Content */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Typography
              variant="h4"
              sx={{ fontWeight: 700, mb: 2, color: "#F8FAFC" }}
            >
              Optimize your strategy using{" "}
              <Box component="span" sx={{ color: "#20B3FF" }}>
                AI-powered trading toolkit
              </Box>
            </Typography>

            <Typography sx={{ mb: 3, color: "#94A3B8" }}>
              From signal alerts to auto risk management, Growth Quantix
              provides every tool you need to trade smarter.
            </Typography>

            <List sx={{ color: "#cbd5e1" }}>
              <ListItem disableGutters>
                <ListItemText primary="✔️ Real-time signal generation with AI strategy engine" />
              </ListItem>
              <ListItem disableGutters>
                <ListItemText primary="✔️ Auto stop loss and target calculations" />
              </ListItem>
              <ListItem disableGutters>
                <ListItemText primary="✔️ Dynamic entry & exit alerts via WhatsApp, Telegram & app" />
              </ListItem>
            </List>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VideoEmbedSection;
