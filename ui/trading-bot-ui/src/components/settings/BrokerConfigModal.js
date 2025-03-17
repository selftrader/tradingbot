import React, { useState, useEffect } from "react";
import { Modal, Box, Typography, TextField, Button, Select, MenuItem, CircularProgress, IconButton } from "@mui/material";
import { Close } from "@mui/icons-material";
import brokerAPI from "../../services/brokerAPI";  // ✅ Use API service

const brokers = ["Zerodha", "Upstox", "Dhan", "Angel One", "Fyers"];
const fields = {
    "Dhan": ["client_id", "access_token"],
    "Zerodha": ["api_key", "api_secret", "request_token"],
    "Upstox": ["api_key", "api_secret"],
    "Angel One": ["api_key", "api_secret", "client_code", "password"],
    "Fyers": ["client_id", "secret_key"]
};

const BrokerConfigModal = ({ open, onClose, refreshBrokers, existingBrokers }) => {
    const [broker, setBroker] = useState({ broker_name: "", credentials: {} });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        setError(""); // Clear errors when modal opens
    }, [open]);

    const handleChange = (field, value) => {
        setBroker(prev => ({
            ...prev,
            credentials: { ...prev.credentials, [field]: value.trim() }
        }));
    };

    // ✅ Log existing brokers to check structure
    console.log("Existing Brokers:", existingBrokers);

    // ✅ Improved duplicate check function
    const isDuplicate = () => {
        return existingBrokers.some(existing => {
            if (existing.broker_name !== broker.broker_name) return false;

            const requiredFields = fields[broker.broker_name] || [];

            // ✅ Extract credentials correctly from the existing broker
            const existingCredentials = existing.config || existing.credentials || {};

            return requiredFields.every(field => 
                existingCredentials[field]?.trim() === broker.credentials[field]?.trim()
            );
        });
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError("");

        if (!broker.broker_name) {
            setError("Please select a broker.");
            setLoading(false);
            return;
        }

        const requiredFields = fields[broker.broker_name] || [];
        const missingFields = requiredFields.filter(field => !broker.credentials[field]);

        if (missingFields.length > 0) {
            setError(`Missing required fields: ${missingFields.join(", ")}`);
            setLoading(false);
            return;
        }

        if (isDuplicate()) {
            setError("This broker account already exists.");
            setLoading(false);
            return;
        }

        try {
            await brokerAPI.addBroker(broker);
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
            <Box sx={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", bgcolor: "white", p: 3, borderRadius: "10px", width: 350 }}>
                <IconButton onClick={onClose} sx={{ position: "absolute", top: 5, right: 5 }}><Close /></IconButton>
                <Typography variant="h6">Add Broker</Typography>
                <Select fullWidth value={broker.broker_name} onChange={(e) => setBroker({ broker_name: e.target.value, credentials: {} })} sx={{ mt: 2 }}>
                    {brokers.map((name) => (<MenuItem key={name} value={name}>{name}</MenuItem>))}
                </Select>
                {fields[broker.broker_name]?.map(field => (
                    <TextField 
                        key={field} 
                        label={field} 
                        fullWidth 
                        onChange={(e) => handleChange(field, e.target.value)} 
                        sx={{ mt: 2 }} 
                    />
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
