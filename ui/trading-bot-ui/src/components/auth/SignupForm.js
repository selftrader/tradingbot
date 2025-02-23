import React, { useState } from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { signup } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const SignupForm = () => {
  const [credentials, setCredentials] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    const response = await signup(credentials);
    if (response.success) {
      navigate("/login"); // Redirect to login after successful signup
    } else {
      setError(response.error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ textAlign: "center", mt: 10, backgroundColor: "#121212", padding: "20px", borderRadius: "10px" }}>
        <Typography variant="h4" sx={{ color: "#ff44ff", fontWeight: "bold" }}>Signup</Typography>
        <TextField
          fullWidth
          label="Username"
          margin="normal"
          variant="outlined"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
        />
        <TextField
          fullWidth
          label="Email"
          margin="normal"
          variant="outlined"
          value={credentials.email}
          onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
        />
        <TextField
          fullWidth
          label="Password"
          type="password"
          margin="normal"
          variant="outlined"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        />
        {error && <Typography color="error">{error}</Typography>}
        <Button fullWidth variant="contained" sx={{ mt: 2, backgroundColor: "#ff44ff", color: "black" }} onClick={handleSignup}>
          Signup
        </Button>
      </Box>
    </Container>
  );
};

export default SignupForm;
