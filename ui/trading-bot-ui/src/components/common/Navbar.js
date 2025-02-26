import React, { useContext, useState, useEffect } from "react";
import { AppBar, Toolbar, Typography, Button, IconButton } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { ThemeContext } from "../../context/ThemeContext";
import { isAuthenticated, logout } from "../../services/authService";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";
import AuthModal from "../auth/AuthModal";

const Navbar = () => {
  const navigate = useNavigate();
  const { darkMode, toggleTheme } = useContext(ThemeContext);
  const [authOpen, setAuthOpen] = useState(false);
  const [loggedIn, setLoggedIn] = useState(isAuthenticated());

  useEffect(() => {
    setLoggedIn(isAuthenticated());  // ✅ Fix: Track login status on refresh
  }, []);

  const handleLogout = () => {
    logout(navigate);  // ✅ Fix: Ensure `navigate` is passed correctly
    setLoggedIn(false);
  };

  return (
    <>
      <AppBar position="static" sx={{ backgroundColor: darkMode ? "#000000" : "#ffffff" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            AI Trading Bot
          </Typography>

          {/* ✅ Light/Dark Mode Toggle Button */}
          <IconButton
            onClick={toggleTheme}
            sx={{
              backgroundColor: darkMode ? "#f4f4f4" : "#222",
              color: darkMode ? "#222" : "#fff",
              borderRadius: "50%",
              padding: "8px",
              marginRight: "10px",
              transition: "0.3s",
              "&:hover": {
                backgroundColor: darkMode ? "#ddd" : "#333",
              },
            }}
          >
            {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>

          {loggedIn ? (
            <>
              <Button component={Link} to="/dashboard" color="inherit">
                Dashboard
              </Button>
              <Button onClick={handleLogout} color="inherit">
                Logout
              </Button>
            </>
          ) : (
            <Button onClick={() => setAuthOpen(true)} color="inherit">
              Login
            </Button>
          )}
        </Toolbar>
      </AppBar>

      <AuthModal open={authOpen} handleClose={() => setAuthOpen(false)} />
    </>
  );
};

export default Navbar;
