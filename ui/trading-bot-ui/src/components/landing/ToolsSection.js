// src/components/landing/ToolsSection.jsx
import { Box, Container, Typography, Grid } from "@mui/material";
import { motion } from "framer-motion";
import insightsIcon from "../../assets/icons/insights.svg";
import automationIcon from "../../assets/icons/automation.svg";
import accuracyIcon from "../../assets/icons/accuracy.svg";

const tools = [
  {
    title: "AI Trade Insights",
    description: "Smart insights based on technical & volume patterns",
    icon: insightsIcon,
  },
  {
    title: "Automated Execution",
    description: "Speed matters. AI executes trades with zero latency",
    icon: automationIcon,
  },
  {
    title: "Adaptive Accuracy",
    description: "Self-learning algorithms that evolve with market shifts",
    icon: accuracyIcon,
  },
];

const ToolsSection = () => {
  return (
    <Box sx={{ py: 10, bgcolor: "#0d1117" }}>
      <Container maxWidth="lg">
        <Typography
          variant="h4"
          sx={{ color: "#00E5FF", fontWeight: 700, textAlign: "center", mb: 6 }}
        >
          Everything You Need to Win
        </Typography>

        <Grid container spacing={4}>
          {tools.map((tool, index) => (
            <Grid item xs={12} md={4} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
              >
                <Box
                  sx={{
                    background: "#161b22",
                    borderRadius: 3,
                    p: 4,
                    height: "100%",
                    color: "#fff",
                    textAlign: "center",
                    border: "1px solid #2c2f36",
                  }}
                >
                  <img
                    src={tool.icon}
                    alt={tool.title}
                    style={{ height: 60, marginBottom: 16 }}
                  />
                  <Typography
                    variant="h6"
                    sx={{ color: "#00E5FF", fontWeight: 600 }}
                  >
                    {tool.title}
                  </Typography>
                  <Typography sx={{ mt: 1, color: "#ccc", fontSize: 14 }}>
                    {tool.description}
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

export default ToolsSection;
