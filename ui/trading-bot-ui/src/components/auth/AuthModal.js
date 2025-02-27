import React, { useState } from "react";
import { Drawer, TextField, Button, Typography, Box, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { login, signup } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const AuthModal = ({ open, handleClose }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [credentials, setCredentials] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleAuth = async () => {
    const response = isLogin ? await login(credentials, navigate) : await signup(credentials);
    if (response.success) {
      handleClose();
      setCredentials({ username: "", email: "", password: "" });
    } else {
      setError(response.error);
    }
  };

  return (
    <Drawer anchor="right" open={open} onClose={handleClose}>
      <Box
        sx={{
          width: 350,
          p: 4,
          backgroundColor: "#ffffff", // ✅ Changed from black to white
          color: "#000000", // ✅ Ensure text is black
          borderRadius: "10px",
          boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)", // ✅ Soft shadow effect
        }}
      >
        <IconButton onClick={handleClose} sx={{ position: "absolute", top: 10, right: 10, color: "#000" }}>
          <CloseIcon />
        </IconButton>

        <Typography variant="h5" sx={{ fontWeight: "bold", mb: 2, color: "#007bff" }}>
          {isLogin ? "Login" : "Sign Up"}
        </Typography>

        {!isLogin && (
          <TextField
            fullWidth
            label="Email"
            variant="outlined"
            margin="normal"
            value={credentials.email}
            onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
            sx={{
              backgroundColor: "#ffffff", // ✅ Ensure white input field
              borderRadius: "5px",
              "& .MuiInputBase-root": {
                color: "#000000", // ✅ Text inside input is black
              },
            }}
          />
        )}

        <TextField
          fullWidth
          label="Username"
          variant="outlined"
          margin="normal"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
          sx={{
            backgroundColor: "#ffffff", // ✅ White background
            borderRadius: "5px",
            "& .MuiInputBase-root": {
              color: "#000000", // ✅ Ensure black text
            },
          }}
        />

        <TextField
          fullWidth
          label="Password"
          type="password"
          variant="outlined"
          margin="normal"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
          sx={{
            backgroundColor: "#ffffff", // ✅ White background
            borderRadius: "5px",
            "& .MuiInputBase-root": {
              color: "#000000", // ✅ Ensure black text
            },
          }}
        />

        {error && <Typography color="error">{error}</Typography>}

        <Button
          fullWidth
          variant="contained"
          sx={{
            mt: 2,
            backgroundColor: "#007bff", // ✅ Changed from dark to professional blue
            color: "#ffffff",
            fontSize: "16px",
            fontWeight: "bold",
            "&:hover": { backgroundColor: "#0056b3" },
          }}
          onClick={handleAuth}
        >
          {isLogin ? "Login" : "Sign Up"}
        </Button>

        <Button
          fullWidth
          sx={{
            mt: 2,
            color: "#007bff", // ✅ Ensure switch option is visible
            "&:hover": { textDecoration: "underline" },
          }}
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? "Need an account? Sign Up" : "Already have an account? Login"}
        </Button>
      </Box>
    </Drawer>
  );
};

export default AuthModal;
