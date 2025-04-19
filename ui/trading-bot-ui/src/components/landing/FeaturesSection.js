import { Box, Grid, Typography, Container } from "@mui/material";
import { Bolt, QueryStats, Timeline } from "@mui/icons-material";

const features = [
  {
    icon: <Bolt fontSize="large" />,
    title: "AI Execution",
    desc: "Lightning-fast order execution with AI precision and signal-driven automation.",
  },
  {
    icon: <QueryStats fontSize="large" />,
    title: "Smart Analysis",
    desc: "Advanced market analysis powered by machine learning and trend detection.",
  },
  {
    icon: <Timeline fontSize="large" />,
    title: "Performance Tracking",
    desc: "Monitor strategy performance, PnL, and improve continuously in real-time.",
  },
];

const FeaturesSection = () => {
  return (
    <Box py={10} sx={{ backgroundColor: "#010d1a", color: "#fff" }}>
      <Container maxWidth="lg">
        <Typography variant="h4" align="center" fontWeight="bold" mb={4}>
          Why Traders Choose Growth Quantix
        </Typography>
        <Grid container spacing={4}>
          {features.map((item, index) => (
            <Grid key={index} item xs={12} md={4}>
              <Box textAlign="center">
                <Box color="#3DE1FF" mb={2}>
                  {item.icon}
                </Box>
                <Typography variant="h6" fontWeight="bold">
                  {item.title}
                </Typography>
                <Typography variant="body2" mt={1} color="gray">
                  {item.desc}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default FeaturesSection;
