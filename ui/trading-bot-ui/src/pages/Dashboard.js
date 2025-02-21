import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, List, ListItem, ListItemText } from '@mui/material';
import StockSelector from '../components/StockSelector';
import TradeControlButtons from '../components/TradeControls';
import LiveChart from '../components/LiveChart';
import TradeLog from '../components/TradeLog';
import { tradingAPI } from '../services/api';

const Dashboard = () => {
  const [selectedStock, setSelectedStock] = useState("");
  const [availableStocks, setAvailableStocks] = useState([]);

  useEffect(() => {
    const loadStocks = async () => {
      try {
        const stocks = await tradingAPI.getAvailableStocks();
        setAvailableStocks(stocks);
      } catch (err) {
        console.error("Error fetching stocks:", err);
      }
    };
    loadStocks();
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
        {/* Available Stocks List */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Available Stocks
            </Typography>
            {availableStocks.length > 0 ? (
              <List>
                {availableStocks.map((stock, idx) => (
                  <ListItem key={idx}>
                    <ListItemText
                      primary={stock.symbol}
                      secondary={stock.name}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography variant="body1">
                No stocks available.
              </Typography>
            )}
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

export default Dashboard;
