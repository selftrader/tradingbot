import React, { useState } from "react";
import {
    Drawer, TextField, Button, Typography, Box, IconButton, Link, Alert, Select,
    MenuItem, InputLabel, FormControl, CircularProgress
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useNavigate } from "react-router-dom"; // ✅ Import useNavigate
import { login, signup, verifyOtp } from "../../services/authService";

const countryCodes = [
    { code: "+1", country: "United States" },
    { code: "+91", country: "India" },
    { code: "+44", country: "United Kingdom" },
    { code: "+61", country: "Australia" },
];

const AuthModal = ({ open, handleClose, onLoginSuccess, isLogin, setIsLogin }) => {
    const navigate = useNavigate(); // ✅ Initialize useNavigate
    const [credentials, setCredentials] = useState({
        fullname: "", identifier: "", phone: "", countryCode: "+1", password: ""
    });
    const [error, setError] = useState("");
    const [showOtpField, setShowOtpField] = useState(false);
    const [otp, setOtp] = useState("");
    const [loading, setLoading] = useState(false);

    // ✅ Handle Input Changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    // ✅ Handle Login or Signup
    const handleAuth = async () => {
        setError("");
        setLoading(true);

        try {
            let response;

            if (isLogin) {
                response = await login({
                    email: credentials.identifier,
                    password: credentials.password
                });

                if (response.success) {
                    handleSuccess();
                }
            } else {
                response = await signup({
                    full_name: credentials.fullname,
                    email: credentials.identifier,
                    phone_number: credentials.phone,
                    country_code: credentials.countryCode,
                    password: credentials.password
                });

                if (response.success) {
                    setShowOtpField(true);
                }
            }

            if (!response.success) {
                handleError(response.message);
            }
        } catch (err) {
            handleError("Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    // ✅ Handle OTP Verification
    const handleOtpVerification = async () => {
        setLoading(true);
        try {
            const response = await verifyOtp(credentials.phone, credentials.countryCode, otp);
            if (response.success) {
                handleSuccess();
            } else {
                handleError(response.message);
            }
        } catch (err) {
            handleError("Invalid OTP. Try again.");
        } finally {
            setLoading(false);
        }
    };

    // ✅ Handle Success (Redirect to Dashboard)
    const handleSuccess = () => {
        console.log("✅ Login Successful, Navigating to /dashboard");
        setShowOtpField(false);
        handleClose();
        setCredentials({ fullname: "", identifier: "", phone: "", countryCode: "+91", password: "" });
        window.dispatchEvent(new Event("storage"));
        onLoginSuccess();

        navigate("/dashboard", { replace: true }); // ✅ Redirect to Dashboard
    };

    // ✅ Handle Errors
    const handleError = (message) => {
        console.log("🔴 API Error Response:", message);
        let errorMessage = "Something went wrong.";

        if (typeof message === "string") {
            errorMessage = message;
        } else if (Array.isArray(message)) {
            errorMessage = message.map(err => err.msg).join(", ");
        } else if (typeof message === "object") {
            errorMessage = JSON.stringify(message);
        }

        setError(errorMessage);
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

                {/* ✅ Error Message */}
                {error && (
                    <Alert severity="error">
                        {typeof error === "string" ? error : "An unexpected error occurred."}
                    </Alert>
                )}

                {!showOtpField ? (
                    <>
                        {!isLogin && (
                            <>
                                <TextField
                                    fullWidth
                                    label="Full Name"
                                    name="fullname"
                                    variant="outlined"
                                    margin="normal"
                                    value={credentials.fullname}
                                    onChange={handleChange}
                                    sx={{ bgcolor: "background.paper" }}
                                />

                                <Box sx={{ display: "flex", gap: 1, alignItems: "center" }}>
                                    <FormControl sx={{ minWidth: 100 }}>
                                        <InputLabel>Country Code</InputLabel>
                                        <Select
                                            name="countryCode"
                                            value={credentials.countryCode}
                                            onChange={handleChange}
                                        >
                                            {countryCodes.map((country) => (
                                                <MenuItem key={country.code} value={country.code}>
                                                    {country.country} ({country.code})
                                                </MenuItem>
                                            ))}
                                        </Select>
                                    </FormControl>

                                    <TextField
                                        fullWidth
                                        label="Phone Number"
                                        name="phone"
                                        variant="outlined"
                                        margin="normal"
                                        value={credentials.phone}
                                        onChange={handleChange}
                                        sx={{ bgcolor: "background.paper" }}
                                    />
                                </Box>
                            </>
                        )}

                        <TextField
                            fullWidth
                            label="Email"
                            name="identifier"
                            variant="outlined"
                            margin="normal"
                            value={credentials.identifier}
                            onChange={handleChange}
                            sx={{ bgcolor: "background.paper" }}
                        />

                        <TextField
                            fullWidth
                            label="Password"
                            name="password"
                            type="password"
                            variant="outlined"
                            margin="normal"
                            value={credentials.password}
                            onChange={handleChange}
                            sx={{ bgcolor: "background.paper" }}
                        />

                        <Button
                            fullWidth
                            variant="contained"
                            sx={{ mt: 2 }}
                            onClick={handleAuth}
                            disabled={loading || !credentials.identifier || !credentials.password}
                        >
                            {loading ? <CircularProgress size={24} sx={{ color: "white" }} /> : isLogin ? "Login" : "Sign Up"}
                        </Button>
                    </>
                ) : (
                    <>
                        <TextField
                            fullWidth
                            label="Enter OTP"
                            name="otp"
                            variant="outlined"
                            margin="normal"
                            value={otp}
                            onChange={(e) => setOtp(e.target.value)}
                            sx={{ bgcolor: "background.paper" }}
                        />

                        <Button
                            fullWidth
                            variant="contained"
                            sx={{ mt: 2 }}
                            onClick={handleOtpVerification}
                            disabled={loading || !otp}
                        >
                            {loading ? <CircularProgress size={24} sx={{ color: "white" }} /> : "Verify OTP"}
                        </Button>
                    </>
                )}

                <Typography variant="body2" sx={{ mt: 2, textAlign: "center", color: "text.primary" }}>
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
