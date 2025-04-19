import { Box, Typography, TextField, Button } from "@mui/material";

const ComplianceForm = () => {
  return (
    <Box id="compliance" sx={{ mt: 4 }}>
      <Typography variant="h6" fontWeight="bold" mb={2}>
        Compliance Query
      </Typography>
      <Typography variant="body2" mb={2}>
        Reach out to our compliance team with security-related questions or
        partnership inquiries.
      </Typography>
      <Box component="form" noValidate autoComplete="off">
        <TextField fullWidth label="Name" sx={{ mb: 2 }} />
        <TextField fullWidth label="Email" sx={{ mb: 2 }} />
        <TextField
          fullWidth
          label="Message"
          multiline
          rows={4}
          sx={{ mb: 2 }}
        />
        <Button variant="contained" color="primary">
          Submit
        </Button>
      </Box>
    </Box>
  );
};

export default ComplianceForm;
