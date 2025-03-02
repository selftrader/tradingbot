import React, { useState } from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { signup } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const SignupForm = () => {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    if (!form.username || !form.email.includes("@") || form.password.length < 8) {
      setError("Please enter valid details.");
      return;
    }

    const response = await signup(form);
    if (response.success) {
      navigate("/login"); // ✅ Redirect to login after successful signup
    } else {
      setError(response.error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ textAlign: "center", mt: 10, padding: "20px", borderRadius: "10px" }}>
        <Typography variant="h4">Signup</Typography>
        <TextField fullWidth label="Username" margin="normal" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
        <TextField fullWidth label="Email" margin="normal" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <TextField fullWidth label="Password" type="password" margin="normal" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        {error && <Typography color="error">{error}</Typography>}
        <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={handleSignup}>
          Signup
        </Button>
      </Box>
    </Container>
  );
};

export default SignupForm;
