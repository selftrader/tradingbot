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
import LiveLTPBatch from "../components/trading/LiveLTPBatch";
const DashboardPage = () => {
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [tradeSettingsOpen, setTradeSettingsOpen] = useState(false);
  const [selectedStockForSettings, setSelectedStockForSettings] =
    useState(null);
  const [trading, setTrading] = useState(false);

  const selectedStocksRef = useRef([]);

  useEffect(() => {
    selectedStocksRef.current = selectedStocks;
  }, [selectedStocks]);

  // ✅ WebSocket callback to update market data
  const updateLTPs = (ltpMap) => {
    setSelectedStocks((prevStocks) =>
      prevStocks.map((stock) => ({
        ...stock,
        livePrice: ltpMap[stock.instrumentKey]?.ltp ?? stock.livePrice,
        volume: ltpMap[stock.instrumentKey]?.volume ?? stock.volume,
        avgPrice: ltpMap[stock.instrumentKey]?.avg_price ?? stock.avgPrice,
        lastUpdate: ltpMap[stock.instrumentKey]?.timestamp
          ? new Date(ltpMap[stock.instrumentKey].timestamp).getTime()
          : stock.lastUpdate,
      }))
    );
  };

  // ✅ Handle Stock Selection
  const handleStockSelect = (stockData) => {
    const alreadyAdded = selectedStocks.some(
      (s) => s.symbol === stockData.symbol && s.exchange === stockData.exchange
    );
    if (alreadyAdded) {
      alert("Stock already added.");
      return;
    }

    const newStock = {
      id: `${stockData.exchange}_${stockData.symbol}`,
      name: stockData.name,
      symbol: stockData.symbol,
      exchange: stockData.exchange,
      instrument: stockData.instrument,
      instrumentKey: stockData.instrumentKey,
      segment: stockData.segment,
      lotSize: stockData.lot_size,
      tickSize: stockData.tick_size,
      livePrice: 0,
      volume: 0,
      avgPrice: 0,
      lastUpdate: null,
      buying: 0,
      selling: 0,
      amount: 0,
      status: "Not Started",
      profitLoss: 0,
    };

    setSelectedStocks((prev) => [...prev, newStock]);
  };

  const handleRemoveStock = (id) => {
    setSelectedStocks((prev) => prev.filter((stock) => stock.id !== id));
  };

  const openTradeSettings = (stock) => {
    setSelectedStockForSettings(stock);
    setTradeSettingsOpen(true);
  };

  const handleStartTrade = () => setTrading(true);
  const handleStopTrade = () => setTrading(false);

  const columns = [
    { field: "name", headerName: "Stock Name", width: 180 },
    { field: "symbol", headerName: "Symbol", width: 120 },
    { field: "exchange", headerName: "Exchange", width: 100 },
    { field: "instrumentKey", headerName: "Instrument", width: 120 },
    {
      field: "livePrice",
      headerName: "Live Price (₹)",
      width: 140,
      renderCell: (params) => (
        <Typography variant="body2">
          ₹{params.row.livePrice || "Loading..."}
        </Typography>
      ),
    },
    {
      field: "volume",
      headerName: "Volume",
      width: 120,
      renderCell: (params) => (
        <Typography variant="body2">
          {params.row.volume?.toLocaleString() || "-"}
        </Typography>
      ),
    },
    {
      field: "avgPrice",
      headerName: "Avg Price (₹)",
      width: 140,
      renderCell: (params) => (
        <Typography variant="body2">₹{params.row.avgPrice || "-"}</Typography>
      ),
    },
    {
      field: "lastUpdate",
      headerName: "Last Update",
      width: 180,
      renderCell: (params) => (
        <Typography variant="body2">
          {params.row.lastUpdate
            ? new Date(params.row.lastUpdate).toLocaleTimeString()
            : "-"}
        </Typography>
      ),
    },
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
      {/* <Typography variant="h4" fontWeight="bold" color="primary" gutterBottom>
        Algo Trading Dashboard
      </Typography> */}

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

      {/* ✅ Live LTP WebSocket Hook */}
      <LiveLTPBatch stocks={selectedStocks} updateLTPs={updateLTPs} />

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
