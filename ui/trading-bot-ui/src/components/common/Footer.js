// src/components/Footer.js
import React from "react";
import { Box, Typography } from "@mui/material";

function Footer() {
  return (
    <Box sx={{ borderTop: "1px solid #333", textAlign: "center", p: 2, mt: 4 }}>
      <Typography variant="body2" sx={{ color: "#aaa" }}>
        &copy; 2025 Trading Bot. All rights reserved.
      </Typography>
    </Box>
  );
}

export default Footer;
