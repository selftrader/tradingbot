import React, { useState } from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { loginUser } from "../../services/authService";

const LoginForm = ({ onLogin }) => {
    const [credentials, setCredentials] = useState({ email: "", password: "" });
    const [error, setError] = useState("");

    const handleLogin = async () => {
        const response = await loginUser(credentials);
        if (response.success) {
            onLogin(response.user);
        } else {
            setError(response.message);
        }
    };

    return (
        <Container>
            <Typography variant="h5">Login to Trading Bot</Typography>
            <Box display="flex" flexDirection="column" gap={2} marginTop={2}>
                <TextField label="Email" variant="outlined" fullWidth 
                    onChange={(e) => setCredentials({ ...credentials, email: e.target.value })} />
                <TextField label="Password" type="password" variant="outlined" fullWidth 
                    onChange={(e) => setCredentials({ ...credentials, password: e.target.value })} />
                {error && <Typography color="error">{error}</Typography>}
                <Button variant="contained" color="primary" onClick={handleLogin}>
                    Login
                </Button>
            </Box>
        </Container>
    );
};

export default LoginForm;
