import React, { useState } from "react";
import {
  Box,
  Container,
  Typography,
  Grid,
  Button,
  Modal,
  useTheme,
} from "@mui/material";
import { motion } from "framer-motion";

// Logos (Replace with your own if available)
import isoLogo from "../../assets/trust/iso.svg";
import sebiLogo from "../../assets/trust/sebi.svg";
import uptimeLogo from "../../assets/trust/uptime.svg";
import shieldLogo from "../../assets/trust/shield.svg";

const trustBadges = [
  {
    name: "ISO Certified",
    logo: isoLogo,
    description:
      "GrowthQuantix is ISO 27001 certified, ensuring top-tier data security, privacy protocols, and IT infrastructure standards.",
  },
  {
    name: "SEBI Compliant",
    logo: sebiLogo,
    description:
      "We operate in accordance with SEBI regulations to ensure all transactions, APIs, and user controls are regulatory compliant.",
  },
  {
    name: "99.99% Uptime",
    logo: uptimeLogo,
    description:
      "Our platform is hosted on globally distributed servers with automatic failovers, guaranteeing ultra-low latency and uptime.",
  },
  {
    name: "Secure Encryption",
    logo: shieldLogo,
    description:
      "We use bank-level AES-256 encryption for all sensitive data and token transmission, ensuring full protection.",
  },
];

const TrustBadgesSection = () => {
  const theme = useTheme();

  const [selectedBadge, setSelectedBadge] = useState(null);

  return (
    <Box
      sx={{
        py: 10,
        bgcolor: theme.palette.background.default,
        color: theme.palette.text.primary,
        textAlign: "center",
        position: "relative",
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="h4" fontWeight="bold" color="primary" mb={4}>
          Why You Can Trust Growth Quantix
        </Typography>

        <Grid container spacing={4} justifyContent="center">
          {trustBadges.map((badge, idx) => (
            <Grid item xs={12} sm={6} md={3} key={idx}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: idx * 0.15 }}
              >
                <Box
                  onClick={() => setSelectedBadge(badge)}
                  sx={{
                    py: 3,
                    px: 2,
                    borderRadius: 3,
                    border: `1px solid ${theme.palette.divider}`,
                    backgroundColor:
                      theme.palette.mode === "dark"
                        ? "rgba(255,255,255,0.04)"
                        : "rgba(0,0,0,0.04)",
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    cursor: "pointer",
                    transition: "all 0.3s",
                    "&:hover": {
                      boxShadow: "0px 0px 20px rgba(0,255,255,0.2)",
                      transform: "scale(1.03)",
                    },
                  }}
                >
                  <Box
                    component="img"
                    src={badge.logo}
                    alt={badge.name}
                    sx={{ width: 50, height: 50, mb: 2, opacity: 0.9 }}
                  />
                  <Typography
                    variant="subtitle1"
                    fontWeight={600}
                    sx={{ mb: 1 }}
                  >
                    {badge.name}
                  </Typography>
                  <Typography
                    variant="body2"
                    sx={{ opacity: 0.7, fontSize: "0.85rem" }}
                  >
                    Tap to learn more
                  </Typography>
                </Box>
              </motion.div>
            </Grid>
          ))}
        </Grid>

        <Button
          variant="contained"
          color="primary"
          size="large"
          href="/security"
          sx={{ mt: 6, borderRadius: "30px", px: 5 }}
        >
          Read Our Security & Compliance
        </Button>
      </Container>

      {/* 🔐 Modal for Badge Detail */}
      <Modal open={!!selectedBadge} onClose={() => setSelectedBadge(null)}>
        <Box
          sx={{
            maxWidth: 500,
            mx: "auto",
            mt: "10%",
            bgcolor: theme.palette.background.paper,
            color: theme.palette.text.primary,
            p: 4,
            borderRadius: 3,
            boxShadow: 24,
          }}
        >
          <Typography variant="h6" fontWeight="bold" mb={2}>
            {selectedBadge?.name}
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.85 }}>
            {selectedBadge?.description}
          </Typography>
          <Button
            fullWidth
            variant="outlined"
            sx={{ mt: 3 }}
            onClick={() => setSelectedBadge(null)}
          >
            Close
          </Button>
        </Box>
      </Modal>
    </Box>
  );
};

export default TrustBadgesSection;
