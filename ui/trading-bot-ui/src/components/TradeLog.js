import React from "react";
import { Paper, Typography } from "@mui/material";

const TradeLog = ({ tradeLog }) => {
  return (
    <Paper sx={{ p: 2, background: "#1E1E1E", color: "white" }}>
      <Typography variant="h6">Trade Executions</Typography>
      {tradeLog.map((trade) => (
        <Paper key={trade.id} sx={{ p: 1, my: 1, background: trade.pnl >= 0 ? "#008000" : "#FF0000" }}>
          <Typography>
            📊 <strong>{trade.stock}</strong> | LTP: ₹{trade.ltp} | Target: ₹{trade.target} | P&L: ₹{trade.pnl} | {trade.notification}
          </Typography>
        </Paper>
      ))}
    </Paper>
  );
};

export default TradeLog;
