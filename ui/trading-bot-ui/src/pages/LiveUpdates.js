import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography } from '@mui/material';
import StockSelector from '../components/StockSelector';
import TradeControlButtons from '../components/TradeControls';
import LiveChart from '../components/LiveChart';
import TradeLog from '../components/TradeLog';

const LiveUpdates = () => {
  // Selected stock from the selector
  const [selectedStock, setSelectedStock] = useState("");

  // Market data state
  const [marketData, setMarketData] = useState({
    price: 100.00,
    marketStatus: "Up, 1.20% change",
    volume: "1.5M Shares",
    lastUpdated: "Not updated yet"
  });

  // Simulate real-time market data updates every 2 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setMarketData(prevData => {
        const fluctuation = (Math.random() - 0.5) * 2;
        const newPrice = Math.round((prevData.price + fluctuation) * 100) / 100;
        const direction = newPrice > prevData.price ? "Up" : "Down";
        const changePercent = Math.abs(((newPrice - prevData.price) / prevData.price) * 100).toFixed(2);
        return {
          price: newPrice,
          marketStatus: `${direction}, ${changePercent}% change`,
          volume: `${(Math.random() * 1 + 1.5).toFixed(1)}M Shares`,
          lastUpdated: new Date().toLocaleTimeString()
        };
      });
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Container sx={{ mt: 4 }}>
      <Grid container spacing={3}>
        {/* Stock Selector */}
        <Grid item xs={12} md={6}>
          <StockSelector onSelect={setSelectedStock} />
        </Grid>
        {/* Trade Control Buttons */}
        <Grid item xs={12} md={6}>
          <TradeControlButtons selectedStock={selectedStock} />
        </Grid>
        {/* Live Chart */}
        <Grid item xs={12}>
          <LiveChart />
        </Grid>
        {/* Live Market Data */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Live Market Data
            </Typography>
            <Typography>Current Price: ₹{marketData.price}</Typography>
            <Typography>Market Status: {marketData.marketStatus}</Typography>
            <Typography>Volume: {marketData.volume}</Typography>
            <Typography>Last Updated: {marketData.lastUpdated}</Typography>
          </Paper>
        </Grid>
        {/* Trade Log */}
        <Grid item xs={12}>
          <TradeLog />
        </Grid>
      </Grid>
    </Container>
  );
};

export default LiveUpdates;