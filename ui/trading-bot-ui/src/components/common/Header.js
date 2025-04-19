import React from "react";
import { AppBar, Toolbar, Typography, Box, Button } from "@mui/material";

const Header = () => {
  return (
    <AppBar
      position="sticky"
      sx={{
        bgcolor: "transparent",
        boxShadow: "none",
        backdropFilter: "blur(10px)",
      }}
    >
      <Toolbar sx={{ justifyContent: "space-between" }}>
        <Typography variant="h6" fontWeight="bold">
          Growth Quantix
        </Typography>
        <Box>
          <Button color="inherit">Features</Button>
          <Button color="inherit">Resources</Button>
          <Button color="inherit">Pricing</Button>
          <Button color="inherit">Login</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
