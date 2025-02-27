import React from "react";
import { Button, Paper, Typography } from "@mui/material";

const TradeControls = ({ stock }) => {
  return (
    <Paper sx={{ padding: 2 }}>
      <Typography variant="h6">Trading Actions</Typography>
      <Button variant="contained" color="primary" sx={{ m: 1 }}>
        Buy {stock.symbol}
      </Button>
      <Button variant="contained" color="error" sx={{ m: 1 }}>
        Sell {stock.symbol}
      </Button>
    </Paper>
  );
};

export default TradeControls; // ✅ Ensure default export
