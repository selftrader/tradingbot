// src/components/Landing/Features.jsx
import { Box, Typography, Grid, Paper } from "@mui/material";

const features = [
  {
    title: "State-of-the-Art Trading Tools",
    desc: "Automated price action, reversal signals, and pro workflows to simplify trading.",
  },
  {
    title: "AI Screeners & Alerts",
    desc: "Find trades with high probability using smart screeners.",
  },
  {
    title: "AI Backtesting Assistant",
    desc: "Build profitable strategies with our proprietary AI agent.",
  },
];

const Features = () => (
  <Box sx={{ py: 10, backgroundColor: "#020617", color: "#fff" }}>
    <Typography variant="h4" textAlign="center" fontWeight="bold" mb={6}>
      Built-in Intelligence with AI
    </Typography>
    <Grid container spacing={4} justifyContent="center">
      {features.map((item, i) => (
        <Grid item xs={12} sm={6} md={4} key={i}>
          <Paper
            sx={{ p: 4, background: "#1e293b", color: "#fff" }}
            elevation={3}
          >
            <Typography variant="h6" fontWeight="bold" mb={1}>
              {item.title}
            </Typography>
            <Typography variant="body2">{item.desc}</Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  </Box>
);

export default Features;
