import React, { useEffect, useState } from "react";
import { Card, CardContent, Typography } from "@mui/material";
import { fetchStockData } from "../../services/stockDataService";

const LiveMarketData = ({ stock }) => {
  const [price, setPrice] = useState(null);
  const [error, setError] = useState(null); // ✅ Track errors

  useEffect(() => {
    const fetchData = async () => {
      const marketData = await fetchStockData(stock);
      if (marketData) {
        setPrice(marketData.lastPrice || marketData.Close);
        setError(null);
      } else {
        setError("Failed to load stock data.");
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Auto-update every 5 sec
    return () => clearInterval(interval);
  }, [stock]);

  return (
    <Card sx={{ minWidth: 275, margin: "10px", backgroundColor: "#121212", color: "white" }}>
      <CardContent>
        <Typography variant="h6">{stock.exchange}: {stock.symbol} Live Price</Typography>
        {error ? (
          <Typography color="error">{error}</Typography>
        ) : (
          <Typography variant="h4" color="primary">
            {price ? `₹${price}` : "Loading..."}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default LiveMarketData;
