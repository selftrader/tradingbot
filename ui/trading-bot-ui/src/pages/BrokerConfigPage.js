import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { Box, Typography, TextField, Button, Card, CardContent, Select, MenuItem, CircularProgress } from "@mui/material";

const BrokerConfigPage = ({ userId }) => {
    const [brokers, setBrokers] = useState([]);
    const [newBroker, setNewBroker] = useState({ broker_name: "", api_key: "", api_secret: "" });
    const [loading, setLoading] = useState(false);

    const availableBrokers = ["Zerodha", "Upstox", "Dhan", "Angel One", "Fyers"];

    // Fetch brokers from API
    const fetchBrokers = useCallback(async () => {
        setLoading(true);
        try {
            const response = await axios.get(`/api/brokers/list/${userId}`);
            setBrokers(response.data);
        } catch (error) {
            console.error("Error fetching brokers:", error);
        } finally {
            setLoading(false);
        }
    }, [userId]);

    useEffect(() => {
        fetchBrokers();
    }, [fetchBrokers]);

    // Add a new broker
    const addBroker = async () => {
        if (!newBroker.broker_name || !newBroker.api_key || !newBroker.api_secret) {
            alert("Please enter all required fields.");
            return;
        }

        try {
            const response = await axios.post("/api/brokers/connect", { user_id: userId, ...newBroker });
            setBrokers((prevBrokers) => [...prevBrokers, response.data]); // Optimistic update
            setNewBroker({ broker_name: "", api_key: "", api_secret: "" });
        } catch (error) {
            console.error("Error adding broker:", error);
        }
    };

    // Delete a broker
    const deleteBroker = async (brokerId) => {
        try {
            await axios.delete(`/api/brokers/disconnect/${brokerId}`);
            setBrokers((prevBrokers) => prevBrokers.filter((broker) => broker.id !== brokerId)); // Optimistic update
        } catch (error) {
            console.error("Error deleting broker:", error);
        }
    };

    return (
        <Box sx={{ p: 4 }}>
            <Typography variant="h4">Broker Configuration</Typography>

            {/* Add Broker Form */}
            <Box sx={{ mt: 3 }}>
                <Typography variant="h6">Add New Broker</Typography>
                <Select
                    fullWidth
                    value={newBroker.broker_name}
                    onChange={(e) => setNewBroker({ ...newBroker, broker_name: e.target.value })}
                    sx={{ mt: 2 }}
                >
                    {availableBrokers.map((broker) => (
                        <MenuItem key={broker} value={broker}>{broker}</MenuItem>
                    ))}
                </Select>
                <TextField
                    fullWidth
                    label="API Key"
                    value={newBroker.api_key}
                    onChange={(e) => setNewBroker({ ...newBroker, api_key: e.target.value })}
                    sx={{ mt: 2 }}
                />
                <TextField
                    fullWidth
                    label="API Secret"
                    type="password"
                    value={newBroker.api_secret}
                    onChange={(e) => setNewBroker({ ...newBroker, api_secret: e.target.value })}
                    sx={{ mt: 2 }}
                />

                <Button variant="contained" sx={{ mt: 2 }} onClick={addBroker}>
                    Add Broker
                </Button>
            </Box>

            {/* Display Brokers */}
            <Typography variant="h5" sx={{ mt: 4 }}>Connected Brokers</Typography>
            {loading ? (
                <CircularProgress sx={{ mt: 2 }} />
            ) : brokers.length > 0 ? (
                brokers.map((broker) => (
                    <Card key={broker.id} sx={{ mt: 2, p: 2 }}>
                        <CardContent>
                            <Typography variant="h6">{broker.broker_name}</Typography>
                            <Button variant="outlined" color="error" sx={{ mt: 1 }} onClick={() => deleteBroker(broker.id)}>
                                Remove
                            </Button>
                        </CardContent>
                    </Card>
                ))
            ) : (
                <Typography>No brokers connected yet.</Typography>
            )}
        </Box>
    );
};

export default BrokerConfigPage;
