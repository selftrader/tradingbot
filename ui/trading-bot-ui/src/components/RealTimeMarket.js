import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";

const RealTimeMarket = () => {
  const [marketData, setMarketData] = useState({ NIFTY: 0, BANKNIFTY: 0 });

  useEffect(() => {
    const fetchMarketData = () => {
      // Simulating market data fetching
      setMarketData({
        NIFTY: (Math.random() * 100 + 18000).toFixed(2),
        BANKNIFTY: (Math.random() * 200 + 40000).toFixed(2),
      });
    };

    fetchMarketData();
    const interval = setInterval(fetchMarketData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ textAlign: "center", marginTop: "2rem" }}>
      <Typography variant="h6">📈 Live Market Data</Typography>
      <Typography variant="body1">NIFTY: {marketData.NIFTY} | BANKNIFTY: {marketData.BANKNIFTY}</Typography>
    </Box>
  );
};

export default RealTimeMarket;
