import { Box, Container, Typography } from "@mui/material";

const AboutSection = () => {
  return (
    <Box py={10} sx={{ backgroundColor: "#071d36", color: "#fff" }}>
      <Container maxWidth="md">
        <Typography variant="h4" align="center" fontWeight="bold" gutterBottom>
          About Growth Quantix
        </Typography>
        <Typography align="center" color="gray" fontSize="1.1rem">
          We’re on a mission to revolutionize algorithmic trading for retail
          traders. With Growth Quantix, you get institutional-grade automation,
          signal-based decision-making, and AI risk management packed into an
          easy-to-use platform.
        </Typography>
      </Container>
    </Box>
  );
};

export default AboutSection;
