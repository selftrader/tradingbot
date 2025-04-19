// src/components/Landing/AIAgentSection.jsx
import React from "react";
import { Box, Container, Typography, Button } from "@mui/material";

const AIAgentSection = () => (
  <Box sx={{ py: 10, bgcolor: "#14161f", color: "#fff" }}>
    <Container maxWidth="md">
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        An AI Agent to build winning strategies
      </Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        Ask GrowthQuantix’s AI Agent to build, test, and optimize strategies
        using backtesters. Unlock smarter, automated decision-making and improve
        win rate.
      </Typography>
      <Button variant="outlined" sx={{ color: "#fff", borderColor: "#00BFFF" }}>
        Get Access Now →
      </Button>
    </Container>
  </Box>
);

export default AIAgentSection;
