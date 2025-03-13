import React, { useState } from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { signup } from "../../services/authService";
import { useNavigate } from "react-router-dom";

const SignupForm = () => {
  const [form, setForm] = useState({ fullname: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    setError("");  // ✅ Clear previous errors

    if (!form.username || !form.email.includes("@") || form.password.length < 8) {
      setError("Please enter valid details.");
      return;
    }

    const response = await signup(form);
    if (response.access_token) {  // ✅ Check for token in response
      localStorage.setItem("token", response.access_token);  // ✅ Store token for authentication
      navigate("/dashboard");  // ✅ Redirect to dashboard after successful signup
    } else {
      setError(response.detail || "Signup failed. Try again.");
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ textAlign: "center", mt: 10, padding: "20px", borderRadius: "10px" }}>
        <Typography variant="h4">Signup</Typography>
        <TextField fullWidth label="Full Name" margin="normal" value={form.fullname} onChange={(e) => setForm({ ...form, fullname: e.target.value })} />
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
