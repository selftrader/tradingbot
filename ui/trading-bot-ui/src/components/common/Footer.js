import React from "react";
import { Box, Container, Typography, Link } from "@mui/material";

const Footer = () => {
  return (
    <Box
      sx={{
        backgroundColor: "#222",
        color: "#ffffff",
        padding: "1.5rem 0",
        marginTop: "auto",
      }}
    >
      <Container maxWidth="lg" sx={{ textAlign: "center" }}>
        <Typography variant="body1">&copy; {new Date().getFullYear()} Trading Bot. All rights reserved.</Typography>
        
        <Typography variant="body2" sx={{ marginTop: "0.5rem", opacity: 0.8 }}>
          <Link href="/terms" sx={{ color: "#bbb", textDecoration: "none", marginRight: "10px" }}>
            Terms & Conditions
          </Link>
          |
          <Link href="/privacy" sx={{ color: "#bbb", textDecoration: "none", marginLeft: "10px" }}>
            Privacy Policy
          </Link>
          |
          <Link href="/contact" sx={{ color: "#bbb", textDecoration: "none", marginLeft: "10px" }}>
            Contact Us
          </Link>
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
