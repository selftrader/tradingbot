import React from "react";
import { Typography, Paper, Box } from "@mui/material";

const MoversTable = ({ stocks }) => {
  const filtered = stocks.filter((s) => s.open && s.livePrice);
  const movers = filtered.map((s) => ({
    ...s,
    changePercent: ((s.livePrice - s.open) / s.open) * 100,
  }));

  const gainers = movers
    .sort((a, b) => b.changePercent - a.changePercent)
    .slice(0, 10);
  const losers = movers
    .sort((a, b) => a.changePercent - b.changePercent)
    .slice(0, 10);

  const renderList = (list, title) => (
    <Box sx={{ width: "48%" }}>
      <Typography variant="h6" color="primary">
        {title}
      </Typography>
      <Paper sx={{ p: 2, mt: 1 }}>
        {list.map((stock, index) => (
          <Box
            key={index}
            display="flex"
            justifyContent="space-between"
            py={0.5}
          >
            <Typography>{stock.symbol}</Typography>
            <Typography>{stock.changePercent.toFixed(2)}%</Typography>
          </Box>
        ))}
      </Paper>
    </Box>
  );

  return (
    <Box display="flex" justifyContent="space-between" mt={4}>
      {renderList(gainers, "📈 Top 10 Gainers")}
      {renderList(losers, "📉 Top 10 Losers")}
    </Box>
  );
};

export default MoversTable;
