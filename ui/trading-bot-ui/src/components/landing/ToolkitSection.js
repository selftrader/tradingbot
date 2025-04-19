import React from "react";
import { Box, Container, Typography, Grid, Paper } from "@mui/material";

const toolkits = [
  {
    title: "Price Action AI",
    desc: "Detects breakouts, retests, and key zones.",
  },
  {
    title: "Signal Overlay Engine",
    desc: "Generates trend-following signals.",
  },
  {
    title: "Oscillator Matrix",
    desc: "Momentum, volume, divergence analytics.",
  },
];

const ToolkitSection = () => {
  return (
    <Box sx={{ bgcolor: "#0a0f1a", color: "#fff", py: 10 }}>
      <Container>
        <Typography variant="h4" fontWeight="bold" align="center" mb={6}>
          AI Toolkit Modules
        </Typography>
        <Grid container spacing={4}>
          {toolkits.map((tool, i) => (
            <Grid item xs={12} md={4} key={i}>
              <Paper
                sx={{ p: 4, bgcolor: "#061120", border: "1px solid #00aeef" }}
              >
                <Typography variant="h6" fontWeight="bold">
                  {tool.title}
                </Typography>
                <Typography sx={{ mt: 2, opacity: 0.85 }}>
                  {tool.desc}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default ToolkitSection;
