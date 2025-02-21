
import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Trading Bot
                </Typography>

                <Button color="inherit" component={RouterLink} to="/">
                    Dashboard
                </Button>
                {/* <Button color="inherit" component={RouterLink} to="/liveupdate">
                    LiveUpdates
                </Button> */}
                <Button color="inherit" component={RouterLink} to="/config">
                    Config
                </Button>
                <Button color="inherit" component={RouterLink} to="/analyze">
                    Analysis
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;