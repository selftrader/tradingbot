import React from "react";
import { Box, Container, Typography, LinearProgress } from "@mui/material";

const metrics = [
  { label: "Backtest Win Rate", value: 82 },
  { label: "Risk Control (Drawdown)", value: 91 },
  { label: "Expected ROI", value: 76 },
  { label: "Latency Optimization", value: 95 },
];

const PerformanceMetricsSection = () => {
  return (
    <Box sx={{ bgcolor: "#010920", color: "#ffffff", py: 10 }}>
      <Container maxWidth="sm">
        <Typography variant="h4" fontWeight="bold" align="center" mb={6}>
          Performance Metrics
        </Typography>
        {metrics.map((m, i) => (
          <Box key={i} sx={{ mb: 4 }}>
            <Typography fontWeight="bold" sx={{ mb: 1 }}>
              {m.label} — {m.value}%
            </Typography>
            <LinearProgress
              variant="determinate"
              value={m.value}
              sx={{
                height: 10,
                borderRadius: 5,
                backgroundColor: "#1a2634",
                "& .MuiLinearProgress-bar": { backgroundColor: "#00AEEF" },
              }}
            />
          </Box>
        ))}
      </Container>
    </Box>
  );
};

export default PerformanceMetricsSection;
