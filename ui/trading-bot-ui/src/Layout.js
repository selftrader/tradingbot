//// filepath: /c:/Work/P/app/tradingapp-main/tradingapp-main/ui/trading-bot-ui/src/Layout.js
import React from 'react';
import { AppBar, Toolbar, Typography, Box, Button, Container } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Layout = ({ children }) => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Trading Bot Dashboard
          </Typography>
          <Button color="inherit" component={RouterLink} to="/">Dashboard</Button>
          <Button color="inherit" component={RouterLink} to="/live-updates">Live Updates</Button>
          <Button color="inherit" component={RouterLink} to="/config">Config</Button>
          <Button color="inherit" component={RouterLink} to="/analysis">Analysis</Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4 }}>
        {children}
      </Container>
    </Box>
  );
};

export default Layout;