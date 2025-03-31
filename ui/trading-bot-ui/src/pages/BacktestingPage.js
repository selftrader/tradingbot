import React, { useState } from "react";
import {
  Container,
  Typography,
  Grid,
  TextField,
  MenuItem,
  Button,
  CircularProgress,
  Paper,
  Divider,
} from "@mui/material";
import axios from "axios";
import StockSearch from "../components/trading/StockSearch";

const BacktestingPage = () => {
  const [interval, setInterval] = useState("1minute");
  const [selectedStock, setSelectedStock] = useState(null);
  const [loading, setLoading] = useState(false);
  const [candles, setCandles] = useState([]);
  const [report, setReport] = useState(null);
  const [tradeLog, setTradeLog] = useState([]);

  const handleRunBacktest = async () => {
    if (!selectedStock) return;

    setLoading(true);
    setReport(null);
    setTradeLog([]);
    setCandles([]);

    try {
      const res = await axios.get(`/api/backtesting/intraday-candles`, {
        params: {
          instrument_key: selectedStock.instrumentKey,
          interval,
        },
      });

      const candleData = res.data.candles || [];
      setCandles(candleData);

      const strategyRes = await axios.post(
        "/api/backtesting/execute-strategy",
        {
          instrument_key: selectedStock.instrumentKey,
          interval,
          candles: candleData,
          strategy: "sma_crossover",
        }
      );

      setReport(strategyRes.data.report || null);
      setTradeLog(strategyRes.data.trades || []);
    } catch (err) {
      console.error("Backtest error:", err);
    }

    setLoading(false);
  };

  return (
    <Container>
      <Typography variant="h4" fontWeight="bold" gutterBottom color="primary">
        Backtesting
      </Typography>

      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={12} md={6}>
          <StockSearch onSearch={(stock) => setSelectedStock(stock)} />
        </Grid>

        <Grid item xs={12} md={3}>
          <TextField
            select
            label="Interval"
            value={interval}
            fullWidth
            onChange={(e) => setInterval(e.target.value)}
          >
            <MenuItem value="1minute">1 Minute</MenuItem>
            <MenuItem value="15minute">15 Minute</MenuItem>
            <MenuItem value="30minute">30 Minute</MenuItem>
            <MenuItem value="day">Day</MenuItem>
            <MenuItem value="week">Week</MenuItem>
            <MenuItem value="month">Month</MenuItem>
          </TextField>
        </Grid>

        <Grid item xs={12} md={3}>
          <Button
            variant="contained"
            color="success"
            fullWidth
            disabled={!selectedStock}
            onClick={handleRunBacktest}
          >
            Run Backtest
          </Button>
        </Grid>
      </Grid>

      {selectedStock && (
        <Paper sx={{ p: 2, mt: 2 }}>
          <Typography variant="subtitle1">
            <strong>Selected Stock:</strong> {selectedStock.symbol} (
            {selectedStock.exchange})
          </Typography>
          <Typography variant="body2">
            <strong>Instrument Key:</strong>{" "}
            {selectedStock.instrumentKey || "Not available"}
          </Typography>
        </Paper>
      )}

      {loading && <CircularProgress sx={{ mt: 3 }} />}

      {report && (
        <Paper sx={{ mt: 4, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            📊 Backtest Report
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <Typography>Total Trades: {report.totalTrades}</Typography>
          <Typography>Profitable Trades: {report.winTrades}</Typography>
          <Typography>Loss Trades: {report.lossTrades}</Typography>
          <Typography>Win Rate: {report.winRate}%</Typography>
          <Typography>Net PnL: ₹{report.netProfit}</Typography>
        </Paper>
      )}

      {tradeLog.length > 0 && (
        <Paper sx={{ mt: 4, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            📋 Trade Log
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <pre
            style={{
              maxHeight: 400,
              overflow: "auto",
              background: "#f0f0f0",
              padding: 8,
              fontSize: 13,
            }}
          >
            {JSON.stringify(tradeLog.slice(0, 20), null, 2)}
          </pre>
        </Paper>
      )}

      {tradeLog.length > 0 && (
        <Paper sx={{ mt: 4, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            📋 Trade Log
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <pre
            style={{
              maxHeight: 400,
              overflow: "auto",
              background: "#f0f0f0",
              padding: 8,
              fontSize: 13,
            }}
          >
            {JSON.stringify(tradeLog.slice(0, 20), null, 2)}
          </pre>
        </Paper>
      )}

      {/* 🔽 Add candle data block here */}
      {candles.length > 0 && (
        <Paper sx={{ mt: 4, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            🕒 Candle Data (First 10)
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <pre
            style={{
              maxHeight: 300,
              overflow: "auto",
              background: "#f9f9f9",
              padding: 8,
              fontSize: 13,
            }}
          >
            {JSON.stringify(candles.slice(0, 10), null, 2)}
          </pre>
        </Paper>
      )}
    </Container>
  );
};

export default BacktestingPage;
