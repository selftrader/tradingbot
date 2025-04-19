import React from "react";
import { Box, Container, Typography, Grid, Paper } from "@mui/material";

const strategies = [
  {
    title: "Index Breakout AI",
    desc: "Scans NIFTY/BANKNIFTY for high-volume breakout patterns.",
  },
  {
    title: "Options Scalper",
    desc: "Uses IV, Delta, Gamma models for fast scalping setups.",
  },
  {
    title: "Sector Rotation Engine",
    desc: "Monitors FII/DII flows and shifts capital between sectors.",
  },
];

const StrategyBacktestingSection = () => {
  return (
    <Box sx={{ bgcolor: "#001427", color: "#fff", py: 10 }}>
      <Container>
        <Typography variant="h4" fontWeight="bold" align="center" mb={6}>
          Strategy & Backtesting Engine
        </Typography>
        <Grid container spacing={4}>
          {strategies.map((s, i) => (
            <Grid item xs={12} md={4} key={i}>
              <Paper
                sx={{ p: 4, bgcolor: "#061120", border: "1px solid #00aeef" }}
              >
                <Typography variant="h6" fontWeight="bold">
                  {s.title}
                </Typography>
                <Typography sx={{ mt: 1, opacity: 0.85 }}>{s.desc}</Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default StrategyBacktestingSection;
