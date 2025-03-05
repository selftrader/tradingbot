import React from "react";
import { Box, Container, Typography, Link, Grid, useTheme, Divider, IconButton } from "@mui/material";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import TwitterIcon from "@mui/icons-material/Twitter";
import FacebookIcon from "@mui/icons-material/Facebook";

const Footer = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        backgroundColor: theme.palette.background.paper,
        color: theme.palette.text.primary,
        padding: { xs: "2rem", md: "3rem" },
        marginTop: "auto",
        textAlign: "center",
        borderTop: `3px solid ${theme.palette.primary.main}`,
        width: "100%",
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4} justifyContent="space-between" alignItems="center">
          {/* Company Info */}
          <Grid item xs={12} md={4} sx={{ textAlign: { xs: "center", md: "left" } }}>
            <Typography variant="h6" sx={{ fontWeight: "bold" }}>
              AI Algo Trading
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8, mt: 1 }}>
              Cutting-edge AI-driven trading platform designed to automate, optimize, and execute profitable trading strategies.
            </Typography>
          </Grid>

          {/* Navigation Links */}
          <Grid item xs={12} md={4}>
            <Typography variant="h6" sx={{ fontWeight: "bold", mb: 1, textAlign: "center" }}>Quick Links</Typography>
            <Grid container spacing={2} justifyContent="center">
              <Grid item>
                <Link href="/terms" sx={{ color: theme.palette.text.secondary, textDecoration: "none", fontWeight: "bold" }}>
                  Terms & Conditions
                </Link>
              </Grid>
              <Grid item>
                <Link href="/privacy" sx={{ color: theme.palette.text.secondary, textDecoration: "none", fontWeight: "bold" }}>
                  Privacy Policy
                </Link>
              </Grid>
              <Grid item>
                <Link href="/contact" sx={{ color: theme.palette.text.secondary, textDecoration: "none", fontWeight: "bold" }}>
                  Contact Us
                </Link>
              </Grid>
            </Grid>
          </Grid>

          {/* Social Media */}
          <Grid item xs={12} md={4} sx={{ textAlign: { xs: "center", md: "right" } }}>
            <Typography variant="h6" sx={{ fontWeight: "bold", mb: 1 }}>Follow Us</Typography>
            <Grid container spacing={1} justifyContent="center" alignItems="center">
              <Grid item>
                <IconButton href="#" sx={{ color: theme.palette.primary.main }}>
                  <LinkedInIcon fontSize="large" />
                </IconButton>
              </Grid>
              <Grid item>
                <IconButton href="#" sx={{ color: theme.palette.primary.main }}>
                  <TwitterIcon fontSize="large" />
                </IconButton>
              </Grid>
              <Grid item>
                <IconButton href="#" sx={{ color: theme.palette.primary.main }}>
                  <FacebookIcon fontSize="large" />
                </IconButton>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
        <Divider sx={{ my: 3, backgroundColor: theme.palette.primary.main, opacity: 0.3 }} />
        {/* Copyright */}
        <Typography variant="body2" sx={{ opacity: 0.7, fontSize: "0.9rem" }}>
          &copy; {new Date().getFullYear()} AI Algo Trading. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
