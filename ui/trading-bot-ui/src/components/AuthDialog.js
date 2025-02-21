import React, { useState } from 'react';
import {
    Dialog,
    Tabs,
    Tab,
    Box,
    TextField,
    Button,
    Alert
} from '@mui/material';
import { tradingAPI } from '../services/api';

const AuthDialog = ({ open, onClose, onLoginSuccess }) => {
    const [tab, setTab] = useState(0);
    const [loginData, setLoginData] = useState({ email: '', password: '' });
    const [signupData, setSignupData] = useState({ name: '', email: '', password: '' });
    const [error, setError] = useState('');

    const handleTabChange = (e, newValue) => {
        setTab(newValue);
        setError('');
    };

    const handleLoginChange = (e) =>
        setLoginData({ ...loginData, [e.target.name]: e.target.value });
    const handleSignupChange = (e) =>
        setSignupData({ ...signupData, [e.target.name]: e.target.value });

    const handleLogin = async () => {
        setError('');
        try {
            const user = await tradingAPI.login(loginData);
            onLoginSuccess(user);
            onClose();
        } catch (err) {
            setError('Login failed. Check your credentials.');
        }
    };

    const handleSignup = async () => {
        setError('');
        try {
            const user = await tradingAPI.signup(signupData);
            onLoginSuccess(user);
            onClose();
        } catch (err) {
            setError('Signup failed. Try again.');
        }
    };

    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={tab} onChange={handleTabChange}>
                    <Tab label="Login" />
                    <Tab label="Sign Up" />
                </Tabs>
            </Box>
            <Box sx={{ p: 3 }}>
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                {tab === 0 ? (
                    <Box>
                        <TextField
                            fullWidth
                            margin="normal"
                            label="Email"
                            name="email"
                            value={loginData.email}
                            onChange={handleLoginChange}
                        />
                        <TextField
                            fullWidth
                            margin="normal"
                            label="Password"
                            type="password"
                            name="password"
                            value={loginData.password}
                            onChange={handleLoginChange}
                        />
                        <Button
                            variant="contained"
                            color="primary"
                            fullWidth
                            onClick={handleLogin}
                        >
                            Login
                        </Button>
                    </Box>
                ) : (
                    <Box>
                        <TextField
                            fullWidth
                            margin="normal"
                            label="Name"
                            name="name"
                            value={signupData.name}
                            onChange={handleSignupChange}
                        />
                        <TextField
                            fullWidth
                            margin="normal"
                            label="Email"
                            name="email"
                            value={signupData.email}
                            onChange={handleSignupChange}
                        />
                        <TextField
                            fullWidth
                            margin="normal"
                            label="Password"
                            type="password"
                            name="password"
                            value={signupData.password}
                            onChange={handleSignupChange}
                        />
                        <Button
                            variant="contained"
                            color="primary"
                            fullWidth
                            onClick={handleSignup}
                        >
                            Sign Up
                        </Button>
                    </Box>
                )}
            </Box>
        </Dialog>
    );
};

export default AuthDialog;