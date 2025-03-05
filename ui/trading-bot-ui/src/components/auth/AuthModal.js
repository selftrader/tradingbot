import React, { useState } from "react";
import { Drawer, TextField, Button, Typography, Box, IconButton, Link } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { login, signup } from "../../services/authService";

const AuthModal = ({ open, handleClose, onLoginSuccess, isLogin, setIsLogin }) => {
  const [credentials, setCredentials] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleAuth = async () => {
    const response = isLogin ? await login(credentials) : await signup(credentials);
    if (response.success) {
      handleClose();  // ✅ Close modal after login
      setCredentials({ email: "", password: "" }); 
      window.dispatchEvent(new Event("storage"));  // ✅ Notify React components
      onLoginSuccess();  // ✅ Navigate to dashboard
    } else {
      setError(response.error);
    }
  };

  return (
    <Drawer anchor="right" open={open} onClose={handleClose}>
      <Box sx={{ width: 350, p: 4, bgcolor: "background.default", color: "text.primary" }}>
        <IconButton onClick={handleClose} sx={{ position: "absolute", top: 10, right: 10 }}>
          <CloseIcon />
        </IconButton>

        <Typography variant="h5" sx={{ fontWeight: "bold", mb: 2 }}>
          {isLogin ? "Login" : "Sign Up"}
        </Typography>

        {!isLogin && (
          <TextField
            fullWidth
            label="Username"
            variant="outlined"
            margin="normal"
            onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
            sx={{ bgcolor: "background.paper" }}
          />
        )}

        <TextField
          fullWidth
          label="Email"
          variant="outlined"
          margin="normal"
          value={credentials.email}
          onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
          sx={{ bgcolor: "background.paper" }}
        />

        <TextField
          fullWidth
          label="Password"
          type="password"
          variant="outlined"
          margin="normal"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
          sx={{ bgcolor: "background.paper" }}
        />

        {error && <Typography color="error">{error}</Typography>}

        <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={handleAuth}>
          {isLogin ? "Login" : "Sign Up"}
        </Button>

        {/* ✅ Improved Login/Signup Toggle for Dark Mode */}
        <Typography
          variant="body2"
          sx={{
            mt: 2,
            textAlign: "center",
            color: "text.primary",
          }}
        >
          {isLogin ? "Need an account? " : "Already have an account? "}
          <Link
            onClick={() => setIsLogin(!isLogin)}
            sx={{
              cursor: "pointer",
              color: "primary.main",
              fontWeight: "bold",
              textDecoration: "underline",
            }}
          >
            {isLogin ? "Sign Up" : "Login"}
          </Link>
        </Typography>
      </Box>
    </Drawer>
  );
};

export default AuthModal;
