import React, { useEffect, useState } from "react";
import { Card, CardContent, Typography } from "@mui/material";
import { fetchMarketData } from "../../services/marketDataService";

const MarketData = ({ symbol }) => {
  const [price, setPrice] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const marketData = await fetchMarketData(symbol);
      if (marketData) setPrice(marketData.price);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Auto-update every 5 sec
    return () => clearInterval(interval);
  }, [symbol]);

  return (
    <Card sx={{ minWidth: 275, margin: "10px" }}>
      <CardContent>
        <Typography variant="h6">{symbol} Live Price</Typography>
        <Typography variant="h4" color="primary">
          {price ? `$${price}` : "Loading..."}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MarketData;