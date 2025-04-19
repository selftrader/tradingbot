// src/pages/ContactPage.jsx
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Grid,
} from "@mui/material";

const ContactPage = () => {
  return (
    <Box sx={{ py: 10, px: 2 }}>
      <Container maxWidth="sm">
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Contact Us
        </Typography>
        <Typography variant="body1" sx={{ mb: 4 }}>
          Have questions, feedback, or partnership inquiries? Reach out below:
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField fullWidth label="Full Name" variant="outlined" />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth label="Email" variant="outlined" />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth label="Phone No." variant="outlined" />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Your Message"
              variant="outlined"
            />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" size="large" fullWidth>
              Send Message
            </Button>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default ContactPage;
