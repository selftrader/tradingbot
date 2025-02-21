//// filepath: /c:/Work/P/app/tradingapp-main/tradingapp-main/ui/trading-bot-ui/src/components/StartTradeButton.js
import React from 'react';
import { Button } from '@mui/material';

const StartTradeButton = ({ selectedStock }) => {
  const startTrade = async () => {
    if (!selectedStock) {
      alert("Please select a stock first.");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/api/start-trade", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Pass in selected stock and any necessary configuration details
        body: JSON.stringify({ stock: selectedStock, config: {} })
      });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error("Error starting trade:", error);
      alert("Error starting trade.");
    }
  };

  return (
    <Button variant="contained" onClick={startTrade}>
      Start Trade
    </Button>
  );
};

export default StartTradeButton;