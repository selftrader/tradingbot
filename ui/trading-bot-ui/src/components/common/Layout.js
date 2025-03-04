import React, { useEffect } from "react";
import { Box, Container, Button, AppBar, Toolbar, Typography } from "@mui/material";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import { isAuthenticated, logout } from "../../services/authService";
import ThemeToggle from "../settings/ThemeToggle";

const Layout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();  // ✅ Clear session and redirect to "/"
  };

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate("/"); // ✅ Redirect to landing page if not authenticated
    }
  }, [navigate]);  // ✅ Fix: Added `navigate` as a dependency

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Navbar />
      <AppBar position="static" sx={{ bgcolor: "primary.main" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, color: "text.primary" }}>
            Trading Bot Dashboard
          </Typography>
          <ThemeToggle />
          {isAuthenticated() ? (
            <>
              <Button color="inherit" component={RouterLink} to="/dashboard">Dashboard</Button>
              <Button color="inherit" onClick={handleLogout}>Logout</Button>
            </>
          ) : (
            <Button color="inherit" component={RouterLink} to="/login">Login</Button>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 10 }}>{children}</Container>
    </Box>
  );
};

export default Layout;
