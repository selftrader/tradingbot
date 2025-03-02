import React from "react";
import { AppBar, Toolbar, Typography, Box, Button, Container } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import { isAuthenticated, logout } from "../../services/authService";

const Layout = ({ children }) => {
  const handleLogout = () => {
    logout();
    window.location.href = "/";
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Trading Bot Dashboard
          </Typography>
          {isAuthenticated() && (
            <>
              <Button color="inherit" component={RouterLink} to="/dashboard">Dashboard</Button>
              <Button color="inherit" component={RouterLink} to="/trade-control">Trade Control</Button>
              <Button color="inherit" component={RouterLink} to="/config">Config</Button>
              <Button color="inherit" onClick={handleLogout}>Logout</Button>
            </>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4 }}>{children}</Container>
    </Box>
  );
};

export default Layout;
