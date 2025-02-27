import React from "react";
import { AppBar, Toolbar, Typography, Box } from "@mui/material";

const Navbar = () => {
  return (
    <AppBar position="sticky" sx={{ background: "#007bff" }}>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Algo Trading Dashboard
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <Typography variant="body1" sx={{ color: "#ffffff" }}>
            NIFTY 50: <span style={{ color: "#28a745" }}>17,710 ▲</span>
          </Typography>
          <Typography variant="body1" sx={{ color: "#ffffff" }}>
            BANKNIFTY: <span style={{ color: "#dc3545" }}>41,500 ▼</span>
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
