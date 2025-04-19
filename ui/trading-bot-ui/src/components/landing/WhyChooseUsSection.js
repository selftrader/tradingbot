import { Box, Typography, Grid } from "@mui/material";

const reasons = [
  "Real-time execution",
  "Dynamic AI model training",
  "Customizable strategies",
  "Risk-managed trading",
  "Intuitive dashboard",
];

const WhyUsSection = () => (
  <Box id="why-us" sx={{ py: 10, px: 4 }}>
    <Typography variant="h4" textAlign="center" fontWeight="bold" mb={4}>
      Why Choose Us?
    </Typography>
    <Grid container spacing={2} justifyContent="center">
      {reasons.map((r, idx) => (
        <Grid item xs={12} sm={6} md={4} key={idx}>
          <Box textAlign="center">
            <Typography fontWeight="bold">{r}</Typography>
          </Box>
        </Grid>
      ))}
    </Grid>
  </Box>
);

export default WhyUsSection;
