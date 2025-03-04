import React, { useState, useEffect } from "react";
import { Container, Typography, Button, Grid, Paper, IconButton } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { Settings, PlayArrow, Stop } from "@mui/icons-material";  // ✅ PlayArrow & Stop now used
import StockSearch from "../components/trading/StockSearch";
import TradeSettingsModal from "../components/trading/TradeSettingsModal";  // ✅ Now used
import { fetchMarketData, fetchLiveStockPrice } from "../services/marketDataService";

const DashboardPage = () => {
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [tradeSettingsOpen, setTradeSettingsOpen] = useState(false);  // ✅ Now used
  const [selectedStockForSettings, setSelectedStockForSettings] = useState(null);  // ✅ Now used
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

  // ✅ Open Trade Settings Modal
  const openTradeSettings = (stock) => {
    setSelectedStockForSettings(stock);
    setTradeSettingsOpen(true);
  };

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
        <IconButton onClick={() => openTradeSettings(params.row)}>  {/* ✅ Now used */}
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

      {/* ✅ Grid Layout for Better Structure */}
      <Grid container spacing={2}>
        <Grid item xs={12} md={8}>
          <StockSearch onSearch={handleStockSelect} />
        </Grid>
        <Grid item xs={12} md={4}>
          <Button variant="contained" color="success" onClick={handleStartTrade} disabled={trading} startIcon={<PlayArrow />}>
            Start Trading
          </Button>
          <Button variant="contained" color="error" onClick={handleStopTrade} disabled={!trading} startIcon={<Stop />}>
            Stop Trading
          </Button>
        </Grid>
      </Grid>

      {/* ✅ Data Grid for Selected Stocks */}
      <Paper sx={{ height: 400, width: "100%", mt: 3, padding: 2, boxShadow: 2 }}>
        <DataGrid rows={selectedStocks} columns={columns} getRowId={(row) => row.id} />
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
