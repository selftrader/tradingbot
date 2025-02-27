import React, { useState } from "react";
import { Container, Grid } from "@mui/material";
import StockSearch from "../components/trading/StockSearch";
import TradeControls from "../components/trading/TradeControls";
import PortfolioTracker from "../components/trading/PortfolioTracker"; // Ensure correct import

const DashboardPage = () => {
  const [stock, setStock] = useState({ symbol: "RELIANCE", exchange: "NSE" });

  return (
    <Container>
      <StockSearch onSearch={setStock} />
      <Grid container spacing={2} sx={{ mt: 3 }}>
        <Grid item xs={12} md={6}>
          <TradeControls stock={stock} />
        </Grid>
        <Grid item xs={12} md={6}>
          <PortfolioTracker />
        </Grid>
      </Grid>
    </Container>
  );
};

export default DashboardPage;
