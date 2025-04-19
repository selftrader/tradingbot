// src/pages/TermsPage.jsx
import { Box, Typography, Container } from "@mui/material";

const TermsPage = () => {
  return (
    <Box sx={{ py: 10, px: 2 }}>
      <Container maxWidth="md">
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Terms & Conditions
        </Typography>
        <Typography variant="body1" sx={{ mb: 2 }}>
          By accessing or using Growth Quantix, you agree to our terms of use.
          These include but are not limited to:
        </Typography>
        <ul>
          <li>
            <Typography variant="body2">
              Users must not use the platform for illegal or manipulative
              trading.
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              Growth Quantix is not liable for market losses or execution
              delays.
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              Violations may result in termination of access.
            </Typography>
          </li>
        </ul>
        <Typography variant="body1" sx={{ mt: 2 }}>
          For full terms, contact legal@growthquantix.com.
        </Typography>
      </Container>
    </Box>
  );
};

export default TermsPage;
