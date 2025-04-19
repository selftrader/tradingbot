// src/pages/PrivacyPolicyPage.jsx
import { Box, Typography, Container } from "@mui/material";

const PrivacyPolicyPage = () => {
  return (
    <Box sx={{ py: 10, px: 2 }}>
      <Container maxWidth="md">
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Privacy Policy
        </Typography>
        <Typography variant="body1" sx={{ mb: 2 }}>
          We take your privacy seriously. Growth Quantix does not sell or share
          your data with third parties without consent.
        </Typography>
        <Typography variant="body1" sx={{ mb: 2 }}>
          We collect only essential information for account creation,
          authentication, and trading functionalities. This data is stored
          securely and encrypted.
        </Typography>
        <Typography variant="body1">
          By using our platform, you agree to our data handling practices as
          outlined here. For questions, contact privacy@growthquantix.com.
        </Typography>
      </Container>
    </Box>
  );
};

export default PrivacyPolicyPage;
