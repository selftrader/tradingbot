// src/components/Landing/StickyNavbar.jsx
import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  useTheme,
} from "@mui/material";
import ThemeToggle from "./ThemeToggle";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../../services/authService";

const StickyNavbar = ({ onAuthOpen }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const isUserLoggedIn = isAuthenticated();

  return (
    <AppBar
      position="fixed"
      elevation={1}
      sx={{
        backdropFilter: "blur(10px)",
        backgroundColor: theme.palette.background.default + "cc", // semi-transparent
        color: theme.palette.text.primary,
      }}
    >
      <Toolbar sx={{ justifyContent: "space-between" }}>
        {/* Logo */}
        <Typography
          variant="h6"
          fontWeight="bold"
          sx={{ cursor: "pointer" }}
          onClick={() => navigate("/")}
        >
          Growth Quantix
        </Typography>

        {/* Right section */}
        <Box display="flex" gap={2} alignItems="center">
          <ThemeToggle />
          {isUserLoggedIn ? (
            <Button variant="contained" onClick={() => navigate("/dashboard")}>
              Dashboard
            </Button>
          ) : (
            <>
              <Button color="primary" onClick={() => onAuthOpen("login")}>
                Sign In
              </Button>
              <Button variant="contained" onClick={() => onAuthOpen("signup")}>
                Get Started
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default StickyNavbar;
