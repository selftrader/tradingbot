import React, { useState, useEffect } from 'react';
import { Box, CircularProgress, Grid, Card, CardContent, Typography } from '@mui/material';
import { tradingAPI } from '../services/api';

const StockSelector = ({ onSelect }) => {
    const [stocks, setStocks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const loadStocks = async () => {
            try {
                const stockData = await tradingAPI.getAvailableStocks();
                setStocks(stockData); // assuming response is an array of stocks
                setError('');
            } catch (err) {
                setError('Failed to load stocks');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        loadStocks();
    }, []);

    if (loading) return <CircularProgress />;
    if (error) return <Typography color="error">{error}</Typography>;

    return (
        <Box sx={{ mt: 2 }}>
            <Typography variant="h6">Select a Stock for Trading</Typography>
            <Grid container spacing={2}>
                {stocks.map((stock) => (
                    <Grid item key={stock.symbol} xs={12} sm={6} md={4}>
                        <Card sx={{ cursor: 'pointer' }} onClick={() => onSelect(stock)}>
                            <CardContent>
                                <Typography variant="h6">{stock.symbol}</Typography>
                                <Typography variant="body2">{stock.name}</Typography>
                                <Typography variant="caption">{stock.sector}</Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default StockSelector;
