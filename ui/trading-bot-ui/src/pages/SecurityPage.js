import React, { useState } from "react";
import {
  Box,
  Typography,
  Container,
  Grid,
  Button,
  Divider,
} from "@mui/material";
import SecuritySidebar from "../components/security/SecuritySidebar";
import ComplianceForm from "../components/security/ComplianceForm";
import auditReport from "../assets/pdf/growthquantix-audit-report.pdf";

const SecurityPage = () => {
  const [activeSection, setActiveSection] = useState("overview");

  return (
    <Box sx={{ py: 8, bgcolor: "background.default", color: "text.primary" }}>
      <Container maxWidth="lg">
        <Typography variant="h4" fontWeight="bold" mb={4}>
          Security & Compliance at Growth Quantix
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12} md={3}>
            <SecuritySidebar
              active={activeSection}
              onNavigate={setActiveSection}
            />
          </Grid>

          <Grid item xs={12} md={9}>
            <Box id="overview" mb={4}>
              <Typography variant="h6" fontWeight="bold" mb={2}>
                Overview
              </Typography>
              <Typography variant="body1" paragraph>
                Growth Quantix is committed to securing your data and
                infrastructure.
              </Typography>
              <Typography variant="body2">
                We follow strict security guidelines, perform regular audits,
                and use enterprise-grade cloud platforms.
              </Typography>
            </Box>

            <Divider sx={{ my: 4 }} />

            <Box id="certifications" mb={4}>
              <Typography variant="h6" fontWeight="bold" mb={2}>
                Certifications
              </Typography>
              <ul>
                <li>✅ ISO 27001 Certified</li>
                <li>✅ SEBI Compliant</li>
                <li>✅ Regular VAPT Audits</li>
              </ul>
              <Button
                variant="outlined"
                color="primary"
                href={auditReport}
                download
                sx={{ mt: 2 }}
              >
                📄 Download Audit Report (PDF)
              </Button>
            </Box>

            <Divider sx={{ my: 4 }} />

            <Box id="infrastructure" mb={4}>
              <Typography variant="h6" fontWeight="bold" mb={2}>
                Infrastructure & Data Security
              </Typography>
              <Typography variant="body2">
                All our APIs and backend systems are hosted on secured AWS/GCP
                instances with data encryption at rest and in transit.
              </Typography>
            </Box>

            <ComplianceForm />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default SecurityPage;
