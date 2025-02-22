import React from "react";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

const Navbar = () => {
  return (
    <AppBar
      position="static"
      sx={{
        background: "rgba(0, 0, 0, 0.8)",
        backdropFilter: "blur(10px)",
        padding: "10px",
        boxShadow: "0px 0px 20px #FF00D6",
      }}
    >
      <Toolbar sx={{ justifyContent: "space-between" }}>
        <Typography
          variant="h5"
          sx={{
            fontWeight: "bold",
            background: "linear-gradient(90deg, #FF00D6, #7C3AED)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Trading Bot
        </Typography>

        <Box sx={{ display: "flex", gap: 3 }}>
          <Button component={RouterLink} to="/" sx={{ color: "#ffffff", "&:hover": { color: "#FF00D6" } }}>
            Dashboard
          </Button>
          <Button component={RouterLink} to="/liveupdate" sx={{ color: "#ffffff", "&:hover": { color: "#7C3AED" } }}>
            Live Updates
          </Button>
          <Button component={RouterLink} to="/config" sx={{ color: "#ffffff", "&:hover": { color: "#7C3AED" } }}>
            Config
          </Button>
          <Button component={RouterLink} to="/analyze" sx={{ color: "#ffffff", "&:hover": { color: "#FF00D6" } }}>
            Analysis
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
