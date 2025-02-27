import React, { useState, useEffect } from "react";
import { Container, Typography, Button, Grid, Paper, IconButton, Box } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid"; // ✅ Excel-style grid
import { Settings, PlayArrow, Stop } from "@mui/icons-material";
import StockSearch from "../components/trading/StockSearch";
import TradeSettingsModal from "../components/trading/TradeSettingsModal";
import { fetchMarketData, fetchLiveStockPrice } from "../services/marketDataService"; // ✅ Fetch stock & live price data

const DashboardPage = () => {
  const [selectedStocks, setSelectedStocks] = useState([]); // ✅ Stores selected stocks
  const [tradeSettingsOpen, setTradeSettingsOpen] = useState(false);
  const [selectedStockForSettings, setSelectedStockForSettings] = useState(null);
  const [trading, setTrading] = useState(false); // ✅ Controls live trading

  // ✅ Search & Add a Stock
  const handleStockSelect = async (symbol, exchange, instrument) => {
    if (selectedStocks.length >= 5) {
      alert("You can track a maximum of 5 stocks.");
      return;
    }

    const stockData = await fetchMarketData(symbol, exchange, instrument);
    setSelectedStocks([...selectedStocks, { ...stockData, status: "Not Started", profitLoss: 0 }]);
  };

  // ✅ Open Trade Settings Modal for a Specific Stock
  const handleOpenSettings = (stock) => {
    if (!stock) return;
    setSelectedStockForSettings(stock);
    setTradeSettingsOpen(true);
  };

  // ✅ Start Trading (Updates Status & Enables Live Updates)
  const handleStartTrade = () => {
    setTrading(true);
    setSelectedStocks(prevStocks =>
      prevStocks.map(stock => ({ ...stock, status: "Trading...", profitLoss: 0 }))
    );
  };

  // ✅ Stop Trading (Stops Updates & Sets Status to Stopped)
  const handleStopTrade = () => {
    setTrading(false);
    setSelectedStocks(prevStocks =>
      prevStocks.map(stock => ({ ...stock, status: "Stopped" }))
    );
  };

  // ✅ Fetch Live Market Prices & Update P&L
  useEffect(() => {
    if (!trading) return;

    const interval = setInterval(async () => {
      setSelectedStocks(prevStocks =>
        prevStocks.map(async stock => {
          const livePrice = await fetchLiveStockPrice(stock.symbol); // ✅ Fetch live price
          const profitLoss = ((livePrice - stock.target) * stock.amount) / stock.target; // ✅ Calculate P&L
          return { ...stock, profitLoss: parseFloat(profitLoss.toFixed(2)) }; // ✅ Update profit/loss
        })
      );
    }, 5000); // ✅ Update every 5 seconds

    return () => clearInterval(interval);
  }, [trading]);

  // ✅ Columns for Excel-Style Grid
  const columns = [
    { field: "symbol", headerName: "Stock", width: 150 },
    { field: "exchange", headerName: "Exchange", width: 120 },
    { field: "instrument", headerName: "Instrument", width: 120 },
    { field: "target", headerName: "Target (₹)", width: 120 },
    { field: "stopLoss", headerName: "Stop Loss (₹)", width: 120 },
    { field: "amount", headerName: "Amount (₹)", width: 120 },
    {
      field: "profitLoss",
      headerName: "P&L (₹)",
      width: 120,
      renderCell: (params) => (
        <Typography color={params.value >= 0 ? "green" : "red"}>{params.value}</Typography>
      ),
    },
    {
      field: "status",
      headerName: "Status",
      width: 130,
      renderCell: (params) => (
        <Typography color={params.value === "Trading..." ? "blue" : "gray"}>{params.value}</Typography>
      ),
    },
    {
      field: "settings",
      headerName: "Settings",
      width: 100,
      renderCell: (params) => (
        <IconButton onClick={() => handleOpenSettings(params.row)}>
          <Settings />
        </IconButton>
      ),
    },
  ];

  return (
    <Container>
      {/* ✅ Header */}
      <Typography variant="h4" sx={{ fontWeight: "bold", color: "#007bff", mb: 3 }}>
        Algo Trading Dashboard
      </Typography>

      {/* ✅ Stock Search & Selection */}
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <StockSearch onSearch={handleStockSelect} />
        </Grid>
      </Grid>

      {/* ✅ Trade Control Buttons */}
      <Box sx={{ display: "flex", justifyContent: "space-between", mt: 3 }}>
        <Button variant="contained" color="success" startIcon={<PlayArrow />} onClick={handleStartTrade} disabled={trading}>
          Start Trading
        </Button>
        <Button variant="contained" color="error" startIcon={<Stop />} onClick={handleStopTrade} disabled={!trading}>
          Stop Trading
        </Button>
      </Box>

      {/* ✅ Excel-Style Stock List */}
      <Paper sx={{ height: 400, width: "100%", mt: 3, padding: 2, boxShadow: 2 }}>
        <Typography variant="h6">Selected Stocks</Typography>
        <DataGrid rows={selectedStocks} columns={columns} getRowId={(row) => row.symbol} />
      </Paper>

      {/* ✅ Trade Settings Modal */}
      <TradeSettingsModal
        open={tradeSettingsOpen}
        onClose={() => setTradeSettingsOpen(false)}
        stock={selectedStockForSettings}
        setSelectedStocks={setSelectedStocks}
      />
    </Container>
  );
};

export default DashboardPage;
