import React, { useState } from "react";
import { Drawer, TextField, Button, Typography, Box, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { login, signup } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const AuthModal = ({ open, handleClose }) => {  // ✅ Fix: Rename `onClose` to `handleClose`
  const [isLogin, setIsLogin] = useState(true);
  const [credentials, setCredentials] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleAuth = async () => {
    const response = isLogin ? await login(credentials, navigate) : await signup(credentials);
    if (response.success) {
      handleClose();  // ✅ Fix: Properly close the modal
      setCredentials({ username: "", email: "", password: "" });  // ✅ Clear fields
    } else {
      setError(response.error);
    }
  };

  return (
    <Drawer anchor="right" open={open} onClose={handleClose}>  
      <Box sx={{ width: 350, p: 4, backgroundColor: "#121212", color: "#fff" }}>
        <IconButton onClick={handleClose} sx={{ position: "absolute", top: 10, right: 10, color: "#fff" }}>
          <CloseIcon />
        </IconButton>
        <Typography variant="h5" sx={{ fontWeight: "bold", mb: 2 }}>
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
          />
        )}

        <TextField
          fullWidth
          label="Username"
          variant="outlined"
          margin="normal"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
        />

        <TextField
          fullWidth
          label="Password"
          type="password"
          variant="outlined"
          margin="normal"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        />

        {error && <Typography color="error">{error}</Typography>}

        <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={handleAuth}>
          {isLogin ? "Login" : "Sign Up"}
        </Button>

        <Button fullWidth sx={{ mt: 2 }} onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? "Need an account? Sign Up" : "Already have an account? Login"}
        </Button>
      </Box>
    </Drawer>
  );
};

export default AuthModal;
