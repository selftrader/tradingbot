import React, { useState, useEffect } from "react";
import { Container, Typography, Button, Grid, Paper, IconButton, Box } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { Settings, PlayArrow, Stop } from "@mui/icons-material";
import StockSearch from "../components/trading/StockSearch";
import TradeSettingsModal from "../components/trading/TradeSettingsModal";
import { fetchMarketData, fetchLiveStockPrice } from "../services/marketDataService";

const DashboardPage = () => {
  const [selectedStocks, setSelectedStocks] = useState([]); 
  const [tradeSettingsOpen, setTradeSettingsOpen] = useState(false);
  const [selectedStockForSettings, setSelectedStockForSettings] = useState(null);
  const [trading, setTrading] = useState(false);

  // ✅ Handle Stock Selection
  const handleStockSelect = async (symbol, exchange, instrument) => {
    if (selectedStocks.length >= 5) {
      alert("You can track a maximum of 5 stocks.");
      return;
    }
    const stockData = await fetchMarketData(symbol, exchange, instrument);
    setSelectedStocks([...selectedStocks, { id: symbol, ...stockData, status: "Not Started", profitLoss: 0 }]);
  };

  // ✅ Start/Stop Trading
  const handleStartTrade = () => setTrading(true);
  const handleStopTrade = () => setTrading(false);

  useEffect(() => {
    if (!trading) return;
    const interval = setInterval(async () => {
      const updatedStocks = await Promise.all(
        selectedStocks.map(async (stock) => {
          const livePrice = await fetchLiveStockPrice(stock.symbol);
          return { ...stock, livePrice };
        })
      );
      setSelectedStocks(updatedStocks);
    }, 5000);
    return () => clearInterval(interval);
  }, [trading, selectedStocks]);

  // ✅ Grid Columns (Fixed Titles)
  const columns = [
    { field: "symbol", headerName: "Stock Symbol", width: 150 },
    { field: "exchange", headerName: "Exchange", width: 120 },
    { field: "instrument", headerName: "Instrument", width: 120 },
    { field: "livePrice", headerName: "Live Price (₹)", width: 120 },
    { field: "target", headerName: "Target Price (₹)", width: 120 },
    { field: "stopLoss", headerName: "Stop Loss (₹)", width: 120 },
    { field: "amount", headerName: "Investment (₹)", width: 120 },
    { field: "status", headerName: "Trading Status", width: 130 },
    { field: "settings", headerName: "Settings", width: 100, renderCell: (params) => (
        <IconButton onClick={() => setSelectedStockForSettings(params.row)}>
          <Settings />
        </IconButton>
      ),
    },
  ];

  return (
    <Container>
      <Typography variant="h4" sx={{ fontWeight: "bold", color: "#007bff", mb: 3 }}>
        Algo Trading Dashboard
      </Typography>
      <StockSearch onSearch={handleStockSelect} />
      <Button variant="contained" color="success" onClick={handleStartTrade} disabled={trading}>Start Trading</Button>
      <Button variant="contained" color="error" onClick={handleStopTrade} disabled={!trading}>Stop Trading</Button>
      <Paper sx={{ height: 400, width: "100%", mt: 3, padding: 2, boxShadow: 2 }}>
        <DataGrid rows={selectedStocks} columns={columns} getRowId={(row) => row.id} />
      </Paper>
    </Container>
  );
};

export default DashboardPage;
