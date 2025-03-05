import React, { useState, useEffect } from "react";
import { AppBar, Toolbar, Typography, IconButton, Menu, MenuItem, Avatar, Button, Box } from "@mui/material";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import ThemeToggle from "../settings/ThemeToggle";
import { getUserProfile } from "../../services/userService";
import { isAuthenticated, logout } from "../../services/authService";

const Navbar = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getUserProfile();
        setUser(data);
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    };
    fetchProfile();
  }, []);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleProfileClick = () => {
    navigate("/profile");
    handleMenuClose();
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <AppBar position="fixed" color="primary">
      <Toolbar sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        {/* <IconButton edge="start" color="inherit" aria-label="menu">
          <MenuIcon />
        </IconButton> */}
        <Typography variant="h6" sx={{ flexGrow: 1 }}>Trading Bot</Typography>
        
        {/* ✅ Navigation Buttons inside Navbar */}
        {isAuthenticated() && (
          <Box sx={{ display: "flex", alignItems: "center", gap: 2, marginLeft: "auto" }}>
            <Button color="inherit" component={RouterLink} to="/dashboard">Dashboard</Button>
            <Button color="inherit" component={RouterLink} to="/trade-control">Trade Control</Button>
            <Button color="inherit" component={RouterLink} to="/config">Config</Button>
            <Button color="inherit" component={RouterLink} to="/analysis">Stock Analysis</Button>
            {/* <Button color="inherit" onClick={handleLogout}>Logout</Button> */}
            <ThemeToggle />
          </Box>
        )}

        {/* Profile Icon */}
        <IconButton onClick={handleMenuOpen} color="inherit">
          <Avatar src={user?.avatar || "/assets/default-avatar.png"} alt="Profile" />
        </IconButton>
        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
          <MenuItem onClick={handleProfileClick}>Profile</MenuItem>
          <MenuItem onClick={handleLogout}>Logout</MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
