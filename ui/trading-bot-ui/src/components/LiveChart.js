import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Typography, Paper } from '@mui/material';
import { subscribeToTradeUpdates } from '../services/api';

const LiveChart = () => {
    const [chartData, setChartData] = useState([]);
    const [tradeUpdate, setTradeUpdate] = useState(null);

    useEffect(() => {
        const unsubscribe = subscribeToTradeUpdates((data) => {
            setChartData(prevData => [...prevData, { time: new Date().toLocaleTimeString(), price: data.price }]);
            setTradeUpdate(data);
        });
        return unsubscribe;
    }, []);

    return (
        <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6">Live Chart</Typography>
            {tradeUpdate ? (
                <Typography variant="body1">
                    {tradeUpdate.message} at {tradeUpdate.time}
                </Typography>
            ) : (
                <Typography variant="body1">Waiting for updates...</Typography>
            )}
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="price" stroke="#8884d8" />
                </LineChart>
            </ResponsiveContainer>
        </Paper>
    );
};

export default LiveChart;
