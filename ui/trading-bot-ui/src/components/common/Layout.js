import React, { useState } from "react";
import { AppBar, Toolbar, Typography, Box, Button, Container, Menu, MenuItem, IconButton, Avatar } from "@mui/material";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { isAuthenticated, logout } from "../../services/authService";
import AuthModal from "../auth/AuthModal"; // ✅ Import login modal
import ProfileModal from "../profile/ProfileModal"; // ✅ Import profile modal

const Layout = () => {
  const navigate = useNavigate();
  const [authOpen, setAuthOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);

  const handleLogout = () => {
    logout();
    navigate("/", { replace: true });
    window.location.reload();
  };

  const handleProfileClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Trading Bot Dashboard
          </Typography>
          {isAuthenticated() ? (
            <>
              <Button color="inherit" component={RouterLink} to="/dashboard">Dashboard</Button>
              <Button color="inherit" component={RouterLink} to="/trade-control">Trade Control</Button>
              <Button color="inherit" component={RouterLink} to="/config">Config</Button>
              <Button color="inherit" component={RouterLink} to="/analysis">Analysis</Button>

              {/* ✅ Profile Icon with Dropdown Menu */}
              <IconButton onClick={handleProfileClick} sx={{ ml: 2 }}>
                <Avatar src="/profile-icon.png" /> {/* Replace with user's actual profile image if available */}
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleProfileClose}
                sx={{ mt: 1 }}
              >
                <MenuItem onClick={() => { setProfileOpen(true); handleProfileClose(); }}>Profile</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </>
          ) : (
            <Button color="inherit" onClick={() => setAuthOpen(true)}>Login</Button>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4 }}></Container>

      {/* ✅ Profile Modal */}
      <ProfileModal open={profileOpen} onClose={() => setProfileOpen(false)} />

      {/* ✅ Login Modal */}
      <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} />
    </Box>
  );
};

export default Layout;
