import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Typography, TextField, Button, Card, CardContent } from "@mui/material";  // ✅ Removed Select & MenuItem

const BrokerConfigPage = () => {
    const [brokers, setBrokers] = useState([]);
    const [newBroker, setNewBroker] = useState({ name: "", apiKey: "", apiSecret: "", trade_percentage: 0 });

    useEffect(() => {
        fetchBrokers();
    }, []);

    const fetchBrokers = () => {
        axios.get("/api/brokers")
            .then(response => setBrokers(response.data))
            .catch(error => console.error("Error fetching brokers:", error));
    };

    const addBroker = () => {
        if (!newBroker.name || !newBroker.apiKey || !newBroker.apiSecret) {
            alert("Please enter all required fields.");
            return;
        }

        axios.post("/api/brokers", newBroker)
            .then(() => {
                fetchBrokers();
                setNewBroker({ name: "", apiKey: "", apiSecret: "", trade_percentage: 0 });
            })
            .catch(error => console.error("Error adding broker:", error));
    };

    const deleteBroker = (brokerId) => {
        axios.delete(`/api/brokers/${brokerId}`)
            .then(() => fetchBrokers())
            .catch(error => console.error("Error deleting broker:", error));
    };

    return (
        <Box sx={{ p: 4 }}>
            <Typography variant="h4">Broker Configuration</Typography>

            <Box sx={{ mt: 3 }}>
                <Typography variant="h6">Add New Broker</Typography>
                <TextField
                    fullWidth
                    label="Broker Name"
                    value={newBroker.name}
                    onChange={(e) => setNewBroker({ ...newBroker, name: e.target.value })}
                    sx={{ mt: 2 }}
                />
                <TextField
                    fullWidth
                    label="API Key"
                    value={newBroker.apiKey}
                    onChange={(e) => setNewBroker({ ...newBroker, apiKey: e.target.value })}
                    sx={{ mt: 2 }}
                />
                <TextField
                    fullWidth
                    label="API Secret"
                    type="password"
                    value={newBroker.apiSecret}
                    onChange={(e) => setNewBroker({ ...newBroker, apiSecret: e.target.value })}
                    sx={{ mt: 2 }}
                />
                <TextField
                    fullWidth
                    label="Trade Allocation (%)"
                    type="number"
                    value={newBroker.trade_percentage}
                    onChange={(e) => setNewBroker({ ...newBroker, trade_percentage: e.target.value })}
                    sx={{ mt: 2 }}
                />

                <Button variant="contained" sx={{ mt: 2 }} onClick={addBroker}>
                    Add Broker
                </Button>
            </Box>

            <Typography variant="h5" sx={{ mt: 4 }}>Existing Brokers</Typography>
            {brokers.length > 0 ? (
                brokers.map((broker) => (
                    <Card key={broker.id} sx={{ mt: 2, p: 2 }}>
                        <CardContent>
                            <Typography variant="h6">{broker.name}</Typography>
                            <Typography>Trade Allocation: {broker.trade_percentage}%</Typography>
                            <Button variant="outlined" color="error" sx={{ mt: 1 }} onClick={() => deleteBroker(broker.id)}>
                                Remove
                            </Button>
                        </CardContent>
                    </Card>
                ))
            ) : (
                <Typography>No brokers configured yet.</Typography>
            )}
        </Box>
    );
};

export default BrokerConfigPage;
