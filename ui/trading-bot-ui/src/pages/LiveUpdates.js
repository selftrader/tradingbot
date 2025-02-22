import React, { useState, useEffect, useRef } from "react";
import { 
  Container, Grid, Paper, Typography, Button, Dialog, DialogActions, 
  DialogContent, DialogTitle, TextField, MenuItem, IconButton, Tooltip 
} from "@mui/material";
import SettingsIcon from "@mui/icons-material/Settings";
import { createChart } from "lightweight-charts";

const indianStocks = [
  { label: "NIFTY 50", value: "NIFTY50" },
  { label: "BANKNIFTY", value: "BANKNIFTY" },
  { label: "Reliance Industries", value: "RELIANCE" },
  { label: "Tata Motors", value: "TATAMOTORS" },
  { label: "Infosys", value: "INFY" },
  { label: "HDFC Bank", value: "HDFCBANK" },
];

const LiveUpdates = () => {
  const [selectedStock, setSelectedStock] = useState("");
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [botRunning, setBotRunning] = useState(false);
  const [tradeLog, setTradeLog] = useState([]);
  const tradeIntervalRef = useRef(null);
  const chartContainerRef = useRef(null);
  const [candleSeries, setCandleSeries] = useState(null);

  const [tradeSettings, setTradeSettings] = useState({
    targetProfit: 5000,
    stopLoss: 2000,
    balance: 100000,
    lotSize: 1,
  });

  const [marketData, setMarketData] = useState({
    price: 100.0,
    open: 98.0,
    high: 102.0,
    low: 97.0,
    close: 100.0,
    volume: "1.5M Shares",
    lastUpdated: "Not updated yet",
  });

  // ✅ Initialize Candlestick Chart
  useEffect(() => {
    if (!chartContainerRef.current || candleSeries) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 300,
      layout: { backgroundColor: "#121212", textColor: "#ffffff" },
      grid: { vertLines: { color: "#444" }, horzLines: { color: "#444" } },
    });

    const series = chart.addCandlestickSeries();
    setCandleSeries(series);

    return () => chart.remove();
  }, []);

  // ✅ Live Market Updates Every 2 Seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setMarketData((prevData) => {
        const fluctuation = (Math.random() - 0.5) * 2;
        const newPrice = Math.round((prevData.price + fluctuation) * 100) / 100;
        const open = prevData.close;
        const high = Math.max(open, newPrice + Math.random() * 2);
        const low = Math.min(open, newPrice - Math.random() * 2);
        const close = newPrice;

        if (candleSeries) {
          candleSeries.update({
            time: Math.floor(Date.now() / 1000),
            open,
            high,
            low,
            close,
          });
        }

        return {
          ...prevData,
          price: newPrice,
          open,
          high,
          low,
          close,
          lastUpdated: new Date().toLocaleTimeString(),
        };
      });
    }, 2000);

    return () => clearInterval(interval);
  }, [candleSeries]);

  // ✅ Handle Start Trading Bot
  const handleStartBot = () => {
    if (!selectedStock) return;
    setBotRunning(true);

    tradeIntervalRef.current = setInterval(() => {
      const pnl = (Math.random() * 500 - 250).toFixed(2);
      const tradeEntry = {
        id: tradeLog.length + 1,
        stock: selectedStock,
        ltp: marketData.price,
        target: tradeSettings.targetProfit,
        pnl: pnl,
        status: pnl >= 0 ? "SUCCESS" : "FAILED",
        notification: pnl >= 0 ? "Trade executed successfully" : "Trade failed due to low balance",
      };
      setTradeLog((prevTrades) => [...prevTrades, tradeEntry]);
    }, 5000);
  };

  // ✅ Handle Stop Trading Bot
  const handleStopBot = () => {
    setBotRunning(false);
    clearInterval(tradeIntervalRef.current);
    tradeIntervalRef.current = null;
  };

  // ✅ Handle Settings Open/Close
  const handleSettingsOpen = () => setSettingsOpen(true);
  const handleSettingsClose = () => setSettingsOpen(false);

  // ✅ Handle Settings Update
  const handleSettingsChange = (e) => {
    setTradeSettings({ ...tradeSettings, [e.target.name]: e.target.value });
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Grid container spacing={3}>
        {/* Stock Selector */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, background: "#121212", color: "white" }}>
            <Typography variant="h6">Select Stock</Typography>
            <TextField
              select
              fullWidth
              value={selectedStock}
              onChange={(e) => setSelectedStock(e.target.value)}
              sx={{ mt: 1, background: "#1E1E1E", color: "white" }}
            >
              {indianStocks.map((stock) => (
                <MenuItem key={stock.value} value={stock.value}>
                  {stock.label}
                </MenuItem>
              ))}
            </TextField>
          </Paper>
        </Grid>

        {/* Settings & Bot Control */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, textAlign: "center", background: "#121212" }}>
            <Typography variant="h6">Trading Controls</Typography>
            
            <Tooltip title="Trading Settings">
              <IconButton onClick={handleSettingsOpen} sx={{ color: "white", mr: 2 }}>
                <SettingsIcon fontSize="large" />
              </IconButton>
            </Tooltip>

            <Button
              variant="contained"
              color={botRunning ? "error" : "success"}
              onClick={botRunning ? handleStopBot : handleStartBot}
              disabled={!selectedStock}
            >
              {botRunning ? "Stop Bot" : "Start Bot"}
            </Button>
          </Paper>
        </Grid>

        {/* Live Candlestick Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, background: "#1E1E1E" }}>
            <Typography variant="h6">Live Candlestick Chart</Typography>
            <div ref={chartContainerRef} style={{ width: "100%", height: "300px" }} />
          </Paper>
        </Grid>

        {/* Trade Execution List */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, background: "#1E1E1E", color: "white" }}>
            <Typography variant="h6">Trade Executions</Typography>
            {tradeLog.map((trade) => (
              <Paper key={trade.id} sx={{ p: 1, my: 1, background: trade.pnl >= 0 ? "#008000" : "#FF0000" }}>
                <Typography>📊 <strong>{trade.stock}</strong> | LTP: ₹{trade.ltp} | P&L: ₹{trade.pnl} | {trade.notification}</Typography>
              </Paper>
            ))}
          </Paper>
        </Grid>
      </Grid>

      {/* ✅ Trading Settings Popup */}
      <Dialog open={settingsOpen} onClose={handleSettingsClose}>
        <DialogTitle>Trading Settings</DialogTitle>
        <DialogContent>
          {Object.keys(tradeSettings).map((key) => (
            <TextField key={key} label={key} name={key} type="number" value={tradeSettings[key]} onChange={handleSettingsChange} fullWidth sx={{ mt: 2 }} />
          ))}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSettingsClose}>Cancel</Button>
          <Button variant="contained" onClick={handleSettingsClose}>Save</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default LiveUpdates;
