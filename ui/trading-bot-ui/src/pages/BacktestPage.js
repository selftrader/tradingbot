import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Box,
  Grid,
  TextField,
  Button,
  Typography,
  Paper,
  CircularProgress,
  Autocomplete,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import ShowChartIcon from "@mui/icons-material/ShowChart";
import { fetchStockList } from "../services/marketDataService";

const API_URL = process.env.REACT_APP_API_URL;

const BacktestingPage = () => {
  const [exchange] = useState("NSE");
  const [instrument] = useState("Equity");
  const [stockList, setStockList] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [fromDate, setFromDate] = useState("2024-01-01");
  const [toDate, setToDate] = useState("2024-03-01");
  const [resultURL, setResultURL] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadStocks = async () => {
      const stocks = await fetchStockList(exchange, instrument);
      setStockList(stocks);
    };
    loadStocks();
  }, []);

  const runBacktest = async () => {
    if (!selectedStock) return;

    try {
      setLoading(true);
      const params = {
        symbol: selectedStock.symbol,
        exchange,
        from_date: fromDate,
        to_date: toDate,
      };

      const res = await axios.get(`${API_URL}/api/backtest/run`, {
        params,
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      setResultURL(url);
    } catch (error) {
      console.error("❌ Error running backtest:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        📊 Backtesting Strategies
      </Typography>

      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Autocomplete
              options={stockList}
              getOptionLabel={(option) => option.symbol}
              value={selectedStock}
              onChange={(event, newValue) => setSelectedStock(newValue)}
              renderInput={(params) => (
                <TextField {...params} label="Select Stock" fullWidth />
              )}
            />
          </Grid>
          <Grid item xs={6} sm={3}>
            <TextField
              fullWidth
              type="date"
              label="From"
              InputLabelProps={{ shrink: true }}
              value={fromDate}
              onChange={(e) => setFromDate(e.target.value)}
            />
          </Grid>
          <Grid item xs={6} sm={3}>
            <TextField
              fullWidth
              type="date"
              label="To"
              InputLabelProps={{ shrink: true }}
              value={toDate}
              onChange={(e) => setToDate(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              fullWidth
              variant="contained"
              color="primary"
              onClick={runBacktest}
              disabled={loading || !selectedStock}
              startIcon={<ShowChartIcon />}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                "Run Backtest"
              )}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {resultURL && (
        <Paper elevation={2} sx={{ p: 3 }}>
          <Typography variant="h6">📈 Backtest Output</Typography>
          <Button
            variant="outlined"
            color="success"
            startIcon={<DownloadIcon />}
            href={resultURL}
            download="backtest_result.csv"
          >
            Download CSV
          </Button>
        </Paper>
      )}
    </Box>
  );
};

export default BacktestingPage;
