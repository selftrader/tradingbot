import React, { useState } from "react";
import { Modal, Box, Typography, TextField, Button, Select, MenuItem, CircularProgress, IconButton } from "@mui/material";
import { Close } from "@mui/icons-material";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const BrokerConfigModal = ({ open, onClose, refreshBrokers }) => {
    const [broker, setBroker] = useState({ broker_name: "", credentials: {} });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const brokers = ["Zerodha", "Upstox", "Dhan", "Angel One", "Fyers"];
    const fields = {
        "Dhan": ["client_id", "access_token"],
        "Zerodha": ["api_key", "api_secret", "request_token"],
        "Upstox": ["api_key", "api_secret"],
        "Angel One": ["api_key", "api_secret", "client_code", "password"],
        "Fyers": ["client_id", "secret_key"]
    };

    const handleChange = (field, value) => {
        setBroker(prev => ({
            ...prev,
            credentials: { ...prev.credentials, [field]: value }
        }));
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError("");

        const token = localStorage.getItem("access_token");

        if (!token) {
            setError("User is not logged in. Please log in first.");
            setLoading(false);
            return;
        }

        try {
            const headers = { Authorization: `Bearer ${token}` };
            await axios.post(`${API_URL}/api/broker/add`, broker, { headers });
            refreshBrokers();
            onClose();
        } catch (error) {
            setError(error.response?.data?.detail || "Failed to add broker");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", bgcolor: "white", p: 3, borderRadius: "10px", width: 300 }}>
                <IconButton onClick={onClose} sx={{ position: "absolute", top: 5, right: 5 }}><Close /></IconButton>
                <Typography variant="h6">Add Broker</Typography>
                <Select fullWidth value={broker.broker_name} onChange={(e) => setBroker({ broker_name: e.target.value, credentials: {} })}>
                    {brokers.map((name) => (<MenuItem key={name} value={name}>{name}</MenuItem>))}
                </Select>
                {fields[broker.broker_name]?.map(field => (
                    <TextField key={field} label={field} fullWidth onChange={(e) => handleChange(field, e.target.value)} sx={{ mt: 2 }} />
                ))}
                {error && <Typography color="error" sx={{ mt: 1 }}>{error}</Typography>}
                <Button variant="contained" fullWidth onClick={handleSubmit} disabled={loading} sx={{ mt: 2 }}>
                    {loading ? <CircularProgress size={20} /> : "Add Broker"}
                </Button>
            </Box>
        </Modal>
    );
};

export default BrokerConfigModal;
