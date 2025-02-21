//// filepath: /c:/Work/P/app/tradingapp-main/tradingapp-main/ui/trading-bot-ui/src/pages/TradeControlPage.js
import React, { useState } from 'react';
import { Container, Paper, Typography, Box, TextField, Button, Stack } from '@mui/material';

const TradeControlForm = () => {
  const [stockSymbol, setStockSymbol] = useState('');
  const [tradeAmount, setTradeAmount] = useState('');

  const handleStartTrade = () => {
    // Replace with your start trade logic
    console.log("Starting trade for stock:", stockSymbol, "with amount:", tradeAmount);
  };

  const handleStopTrade = () => {
    // Replace with your stop trade logic
    console.log("Stopping trade for stock:", stockSymbol);
  };

  return (
    <Box component="form" noValidate sx={{ mt: 2 }}>
      <Stack spacing={2}>
        <TextField
          label="Stock Symbol"
          variant="outlined"
          fullWidth
          value={stockSymbol}
          onChange={(e) => setStockSymbol(e.target.value)}
        />
        <TextField
          label="Trade Amount"
          variant="outlined"
          type="number"
          fullWidth
          value={tradeAmount}
          onChange={(e) => setTradeAmount(e.target.value)}
        />
        <Stack direction="row" spacing={2}>
          <Button variant="contained" color="primary" onClick={handleStartTrade}>
            Start Trade
          </Button>
          <Button variant="outlined" color="secondary" onClick={handleStopTrade}>
            Stop Trade
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
};

const TradeControlPage = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" align="center" gutterBottom>
          Trade Controls
        </Typography>
        <TradeControlForm />
      </Paper>
    </Container>
  );
};

export default TradeControlPage;