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
    setLoggedIn(isAuthenticated());
  }, []);

  const handleLogout = () => {
    logout();
    setLoggedIn(false);
    navigate("/");
  };

  return (
    <>
      <AppBar position="static" sx={{ backgroundColor: darkMode ? "#000000" : "#ffffff" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: "bold", color: darkMode ? "#ff44ff" : "#6a11cb" }}>
            Trading Bot AI
          </Typography>
          {loggedIn ? (
            <Button sx={{ color: darkMode ? "white" : "black" }} onClick={handleLogout}>
              Logout
            </Button>
          ) : (
            <Button sx={{ color: darkMode ? "white" : "black" }} onClick={() => setAuthOpen(true)}>
              Login / Signup
            </Button>
          )}
          <IconButton onClick={toggleTheme}>
            {darkMode ? <LightModeIcon sx={{ color: "#ff44ff" }} /> : <DarkModeIcon sx={{ color: "#6a11cb" }} />}
          </IconButton>
        </Toolbar>
      </AppBar>
      <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} />
    </>
  );
};

export default Navbar;
