import React, { useState } from "react";
import { AppBar, Toolbar, Typography, IconButton, Menu, MenuItem, Avatar } from "@mui/material";
import { Menu as MenuIcon } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import ThemeToggle from "../settings/ThemeToggle";

const Navbar = ({ toggleTheme, isDarkMode }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();

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
    // Add logout functionality here
    handleMenuClose();
  };

  return (
    <>
      <AppBar position="fixed" color="primary">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1, textAlign: { xs: "center", md: "left" } }}>
            Algo Trading Bot
          </Typography>
          <ThemeToggle toggleTheme={toggleTheme} isDarkMode={isDarkMode} />

          {/* Profile Icon with Dropdown */}
          <IconButton onClick={handleMenuOpen} color="inherit">
            <Avatar alt="Profile" src="/path/to/profile-pic.jpg" />
          </IconButton>
          <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
            <MenuItem onClick={handleProfileClick}>Profile</MenuItem>
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
    </>
  );
};

export default Navbar;
