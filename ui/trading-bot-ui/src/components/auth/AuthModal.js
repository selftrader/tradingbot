import React, { useState } from "react";
import { Drawer, TextField, Button, Typography, Box, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { login, signup } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const AuthModal = ({ open, onClose }) => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between login/signup
  const [credentials, setCredentials] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleAuth = async () => {
    const response = isLogin ? await login(credentials) : await signup(credentials);
    if (response.success) {
      onClose(); // Close modal on success
      if (!isLogin) navigate("/dashboard");
    } else {
      setError(response.error);
    }
  };

  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <Box sx={{ width: 350, p: 4, backgroundColor: "#121212", height: "100vh" }}>
        <IconButton onClick={onClose} sx={{ position: "absolute", right: 10, top: 10 }}>
          <CloseIcon sx={{ color: "#ff44ff" }} />
        </IconButton>
        <Typography variant="h4" sx={{ color: "#ff44ff", fontWeight: "bold", textAlign: "center", mb: 3 }}>
          {isLogin ? "Login" : "Create Account"}
        </Typography>
        {!isLogin && (
          <TextField
            fullWidth
            label="Email"
            margin="normal"
            variant="outlined"
            sx={{ input: { color: "white" }, label: { color: "grey" } }}
            value={credentials.email}
            onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
          />
        )}
        <TextField
          fullWidth
          label="Username"
          margin="normal"
          variant="outlined"
          sx={{ input: { color: "white" }, label: { color: "grey" } }}
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
        />
        <TextField
          fullWidth
          label="Password"
          type="password"
          margin="normal"
          variant="outlined"
          sx={{ input: { color: "white" }, label: { color: "grey" } }}
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        />
        {error && <Typography color="error">{error}</Typography>}
        <Button
          fullWidth
          variant="contained"
          sx={{ mt: 2, backgroundColor: "#ff44ff", color: "black" }}
          onClick={handleAuth}
        >
          {isLogin ? "Login" : "Signup"}
        </Button>
        <Typography sx={{ textAlign: "center", mt: 2 }}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <Button sx={{ color: "#ff44ff" }} onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? "Create Account" : "Login"}
          </Button>
        </Typography>
      </Box>
    </Drawer>
  );
};

export default AuthModal;
