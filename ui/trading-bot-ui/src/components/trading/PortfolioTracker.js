import React, { useState } from "react";
import { Card, CardContent, Typography, Button } from "@mui/material";

const PortfolioTracker = () => {
  const [watchlist, setWatchlist] = useState([]);

  const addStock = (symbol) => {
    if (!watchlist.includes(symbol)) {
      setWatchlist([...watchlist, symbol]);
    }
  };

  return (
    <Card sx={{ minWidth: 275, margin: "10px", backgroundColor: "#121212", color: "white" }}>
      <CardContent>
        <Typography variant="h6">Stock Watchlist</Typography>
        {watchlist.length === 0 ? (
          <Typography>No stocks added yet.</Typography>
        ) : (
          watchlist.map((stock, index) => (
            <Typography key={index} variant="body1">• {stock}</Typography>
          ))
        )}
        <Button onClick={() => addStock("RELIANCE")}>Add RELIANCE</Button>
      </CardContent>
    </Card>
  );
};

export default PortfolioTracker;
