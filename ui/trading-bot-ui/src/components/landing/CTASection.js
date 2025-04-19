import { Box, Container, Typography, Button } from "@mui/material";

const CTASection = () => {
  return (
    <Box
      id="cta"
      sx={{
        py: 12,
        background: "linear-gradient(to right, #00AEEF, #005072)",
        color: "white",
      }}
    >
      <Container sx={{ textAlign: "center" }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Start your AI trading journey today
        </Typography>
        <Typography variant="body1" gutterBottom>
          Join thousands of traders using Growth Quantix
        </Typography>
        <Button
          variant="contained"
          sx={{ mt: 2, backgroundColor: "#fff", color: "#005072" }}
        >
          Get Started
        </Button>
      </Container>
    </Box>
  );
};

export default CTASection;
