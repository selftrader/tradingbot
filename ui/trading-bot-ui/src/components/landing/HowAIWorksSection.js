import React from "react";
import { Box, Container, Typography, Grid, Paper } from "@mui/material";

const steps = [
  {
    title: "1. Data Ingestion",
    desc: "Real-time prices, options, sentiment, news feeds.",
  },
  {
    title: "2. Feature Engineering",
    desc: "Transform market behavior into AI-understandable features.",
  },
  {
    title: "3. AI Model Prediction",
    desc: "Run classification/regression models on trade setup opportunities.",
  },
  {
    title: "4. Smart Execution",
    desc: "Send signal or place trade via broker API with stop/risk logic.",
  },
];

const HowAIWorksSection = () => {
  return (
    <Box sx={{ bgcolor: "#001f3f", color: "#fff", py: 10 }}>
      <Container>
        <Typography variant="h4" fontWeight="bold" align="center" mb={6}>
          How Our AI Works
        </Typography>
        <Grid container spacing={4}>
          {steps.map((step, i) => (
            <Grid item xs={12} md={3} key={i}>
              <Paper
                sx={{ p: 4, bgcolor: "#061120", border: "1px solid #00aeef" }}
              >
                <Typography variant="h6" fontWeight="bold">
                  {step.title}
                </Typography>
                <Typography sx={{ mt: 2, opacity: 0.85 }}>
                  {step.desc}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default HowAIWorksSection;
