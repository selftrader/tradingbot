import React, { useState } from "react";
import { Container, Grid } from "@mui/material";
import StockSearch from "../components/trading/StockSearch";
import LiveMarketData from "../components/trading/LiveMarketData";
import TradingViewChart from "../components/trading/TradingViewChart";

const DashboardPage = () => {
  const [stock, setStock] = useState({ symbol: "RELIANCE", exchange: "NSE" });

  return (
    <Container>
      <StockSearch onSearch={setStock} />
      <Grid container spacing={2} sx={{ mt: 3 }}>
        <Grid item xs={12} md={6}>
          <LiveMarketData stock={stock} />
        </Grid>
        <Grid item xs={12} md={6}>
          <TradingViewChart symbol={stock.symbol} exchange={stock.exchange} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default DashboardPage;
