// src/components/Features.js
import React from "react";
import { Box, Typography, Grid, Paper } from "@mui/material";

function Features() {
  const features = [
    { title: "Live Market Analysis", description: "Get real-time market insights with AI predictions." },
    { title: "Automated Trading", description: "Execute trades automatically based on AI signals." },
    { title: "Customizable Strategies", description: "Modify and fine-tune trading strategies with ease." }
  ];

  return (
    <Box sx={{ px: 6, py: 4 }}>
      <Typography variant="h4" sx={{ textAlign: "center", mb: 4 }}>
        Why Choose Our AI Trading Bot?
      </Typography>

      <Grid container spacing={4}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Paper sx={{ p: 3, textAlign: "center", background: "#111" }}>
              <Typography variant="h6" sx={{ color: "primary.main" }}>{feature.title}</Typography>
              <Typography variant="body2" sx={{ color: "text.secondary", mt: 1 }}>{feature.description}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default Features;
