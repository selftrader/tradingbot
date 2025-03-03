import React, { useEffect } from "react";
import { Box, Container, Button, AppBar, Toolbar, Typography } from "@mui/material";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import { isAuthenticated, logout } from "../../services/authService";
import ThemeToggle from "../settings/ThemeToggle";

const Layout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/", { replace: true }); // ✅ Ensures proper navigation
  };

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate("/"); // ✅ Redirect to landing page if not authenticated
    }
  }, []); // ✅ Ensures navigation is enforced on logout

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Navbar />
      <AppBar position="static" sx={{ bgcolor: "primary.main" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, color: "text.primary" }}>Trading Bot Dashboard</Typography>
          <ThemeToggle />
          {isAuthenticated() ? (
            <>
              <Button color="inherit" component={RouterLink} to="/dashboard" sx={{ color: "text.primary" }}>Dashboard</Button>
              <Button color="inherit" component={RouterLink} to="/trade-control" sx={{ color: "text.primary" }}>Trade Control</Button>
              <Button color="inherit" component={RouterLink} to="/config" sx={{ color: "text.primary" }}>Config</Button>
              <Button color="inherit" onClick={handleLogout} sx={{ color: "text.primary" }}>Logout</Button>
            </>
          ) : (
            <Button color="inherit" component={RouterLink} to="/login" sx={{ color: "text.primary" }}>Login</Button>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 10 }}>{children}</Container>
    </Box>
  );
};

export default Layout;
