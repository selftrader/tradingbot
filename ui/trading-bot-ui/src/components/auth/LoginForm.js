import React, { useState } from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { login } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const LoginForm = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    const response = await login(credentials);
    if (response.success) {
      onLogin();
      navigate("/");
    } else {
      setError(response.error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          textAlign: "center",
          mt: 10,
          backgroundColor: "#ffffff", // ✅ Forced white background
          padding: "30px",
          borderRadius: "10px",
          boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)", // ✅ Added light shadow
        }}
      >
        <Typography variant="h4" sx={{ color: "#007bff", fontWeight: "bold" }}>
          Login
        </Typography>

        {/* ✅ Username Input */}
        <TextField
          fullWidth
          label="Username"
          margin="normal"
          variant="outlined"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
          sx={{
            backgroundColor: "#ffffff", // ✅ Light input background
            borderRadius: "5px",
            "& .MuiInputBase-root": {
              color: "#000000", // ✅ Ensure text is black
            },
          }}
        />

        {/* ✅ Password Input */}
        <TextField
          fullWidth
          label="Password"
          type="password"
          margin="normal"
          variant="outlined"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
          sx={{
            backgroundColor: "#ffffff", // ✅ Light input background
            borderRadius: "5px",
            "& .MuiInputBase-root": {
              color: "#000000", // ✅ Ensure text is black
            },
          }}
        />

        {error && <Typography color="error">{error}</Typography>}

        {/* ✅ Login Button */}
        <Button
          fullWidth
          variant="contained"
          sx={{
            mt: 3,
            backgroundColor: "#007bff", // ✅ Changed from pink to blue
            color: "#ffffff",
            fontSize: "16px",
            fontWeight: "bold",
            "&:hover": { backgroundColor: "#0056b3" },
          }}
          onClick={handleLogin}
        >
          Login
        </Button>
      </Box>
    </Container>
  );
};

export default LoginForm;
