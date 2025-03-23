import React, { useState, useEffect, useRef } from "react";
import {
  Container,
  Typography,
  Button,
  Grid,
  Paper,
  IconButton,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { Settings, PlayArrow, Stop, Delete } from "@mui/icons-material";
import StockSearch from "../components/trading/StockSearch";
import TradeSettingsModal from "../components/trading/TradeSettingsModal";
import {
  fetchStockSnapshot,
  fetchLiveStockPrice,
} from "../services/marketDataService";

const DashboardPage = () => {
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [tradeSettingsOpen, setTradeSettingsOpen] = useState(false);
  const [selectedStockForSettings, setSelectedStockForSettings] =
    useState(null);
  const [trading, setTrading] = useState(false);

  const selectedStocksRef = useRef([]);

  // Keep ref in sync with state
  useEffect(() => {
    selectedStocksRef.current = selectedStocks;
  }, [selectedStocks]);

  // ✅ Handle Stock Selection
  const handleStockSelect = async (symbol, exchange, instrument) => {
    if (selectedStocks.length >= 5) {
      alert("You can track a maximum of 5 stocks.");
      return;
    }

    const alreadyAdded = selectedStocks.some(
      (s) => s.symbol === symbol && s.exchange === exchange
    );
    if (alreadyAdded) {
      alert("Stock already added.");
      return;
    }

    try {
      const stockData = await fetchStockSnapshot(symbol);
      if (!stockData || stockData.error) {
        alert("Failed to fetch stock details: " + (stockData?.error || ""));
        return;
      }

      const newStock = {
        id: `${symbol}_${exchange}`,
        name: stockData.name || symbol,
        symbol,
        exchange,
        instrument,
        livePrice: stockData.livePrice || 0,
        target: 0,
        stopLoss: 0,
        amount: 0,
        status: "Not Started",
        profitLoss: 0,
      };

      setSelectedStocks((prev) => [...prev, newStock]);
    } catch (error) {
      console.error("Stock add failed", error);
      alert("Unexpected error while adding stock.");
    }
  };

  // ✅ Remove stock from list
  const handleRemoveStock = (id) => {
    setSelectedStocks((prev) => prev.filter((stock) => stock.id !== id));
  };

  // ✅ Open modal
  const openTradeSettings = (stock) => {
    setSelectedStockForSettings(stock);
    setTradeSettingsOpen(true);
  };

  // ✅ Start/Stop trading
  const handleStartTrade = () => setTrading(true);
  const handleStopTrade = () => setTrading(false);

  // ✅ Real-time price updates
  useEffect(() => {
    if (!trading) return;

    const interval = setInterval(async () => {
      const updated = await Promise.all(
        selectedStocksRef.current.map(async (stock) => {
          try {
            const price = await fetchLiveStockPrice(
              stock.symbol,
              stock.exchange,
              stock.instrument
            );
            return { ...stock, livePrice: price };
          } catch {
            return stock;
          }
        })
      );
      setSelectedStocks(updated);
    }, 5000);

    return () => clearInterval(interval);
  }, [trading]);

  // ✅ DataGrid columns
  const columns = [
    { field: "name", headerName: "Stock Name", width: 180 },
    { field: "symbol", headerName: "Symbol", width: 120 },
    { field: "exchange", headerName: "Exchange", width: 100 },
    { field: "instrument", headerName: "Instrument", width: 120 },
    { field: "livePrice", headerName: "Live Price (₹)", width: 120 },
    { field: "target", headerName: "Target (₹)", width: 120 },
    { field: "stopLoss", headerName: "Stop Loss (₹)", width: 120 },
    { field: "amount", headerName: "Amount (₹)", width: 120 },
    { field: "status", headerName: "Status", width: 130 },
    {
      field: "settings",
      headerName: "Settings",
      width: 90,
      renderCell: (params) => (
        <IconButton onClick={() => openTradeSettings(params.row)}>
          <Settings />
        </IconButton>
      ),
    },
    {
      field: "remove",
      headerName: "Remove",
      width: 80,
      renderCell: (params) => (
        <IconButton onClick={() => handleRemoveStock(params.row.id)}>
          <Delete />
        </IconButton>
      ),
    },
  ];

  return (
    <Container>
      <Typography variant="h4" fontWeight="bold" color="primary" gutterBottom>
        Algo Trading Dashboard
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} sm={8}>
          <StockSearch onSearch={handleStockSelect} />
        </Grid>

        <Grid item xs={6} sm={2}>
          <Button
            fullWidth
            variant="contained"
            color="success"
            onClick={handleStartTrade}
            disabled={trading}
            startIcon={<PlayArrow />}
          >
            Start
          </Button>
        </Grid>
        <Grid item xs={6} sm={2}>
          <Button
            fullWidth
            variant="contained"
            color="error"
            onClick={handleStopTrade}
            disabled={!trading}
            startIcon={<Stop />}
          >
            Stop
          </Button>
        </Grid>
      </Grid>

      <Paper sx={{ mt: 4, height: 430, padding: 2 }}>
        <DataGrid
          rows={selectedStocks}
          columns={columns}
          getRowId={(row) => row.id}
          disableRowSelectionOnClick
        />
      </Paper>

      {/* ✅ Trade Settings Modal */}
      {tradeSettingsOpen && (
        <TradeSettingsModal
          open={tradeSettingsOpen}
          onClose={() => setTradeSettingsOpen(false)}
          stock={selectedStockForSettings}
          setSelectedStocks={setSelectedStocks}
        />
      )}
    </Container>
  );
};

export default DashboardPage;
