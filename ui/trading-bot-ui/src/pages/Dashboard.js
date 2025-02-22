import { Typography, Box } from "@mui/material";

const Dashboard = () => {
  return (
    <Box
      sx={{
        height: "90vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        background: "linear-gradient(to bottom, #000000, #0a0a0a)",
      }}
    >
      <Typography
        variant="h2"
        sx={{
          fontWeight: "bold",
          background: "linear-gradient(to right, #FF00D6, #7C3AED)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
        }}
      >
        AI-Powered Trading Dashboard
      </Typography>
      <Typography variant="h5" sx={{ color: "#ffffff", mt: 2 }}>
        Automated Trades. Real-time Insights.
      </Typography>
    </Box>
  );
};

export default Dashboard;
