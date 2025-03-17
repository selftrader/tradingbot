import React, { useState, useEffect } from "react";
import tradingAPI from "../services/tradingAPI";  
import { analyzeSectoralOptions } from "../services/sectorAnalysisAPI";
import {
    Container,
    Paper,
    Typography,
    Box,
    Button,
    Alert,
    Autocomplete,
    TextField,
    Divider,
    Select,
    MenuItem
} from "@mui/material";
import { PlayArrow } from "@mui/icons-material";

const StockAnalysisPage = () => {
  const [sector, setSector] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [tradingStarted, setTradingStarted] = useState(false);
  const [tradingError, setTradingError] = useState("");  // ✅ Still required
  const [availableStocks, setAvailableStocks] = useState([]);

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const stocks = await tradingAPI.getAvailableStocks();
        setAvailableStocks(stocks);
      } catch (err) {
        setError("Failed to fetch available stocks: " + err.message);
      }
    };
    fetchStocks();
  }, []);

  const handleSectorChange = (e) => {
    setSector(e.target.value);
  };

  const handleAnalyze = async () => {
    if (!sector) {
      setError("Please select a sector.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const result = await analyzeSectoralOptions(sector);
      setAnalysisResult(result);
    } catch (err) {
      setError("Analysis failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStockSelect = (stock) => {
    setSelectedStocks((prev) =>
      prev.includes(stock) ? prev.filter((s) => s !== stock) : [...prev, stock]
    );
  };

  const handleStartTrading = async () => {
    if (selectedStocks.length === 0) {
      setTradingError("Please select at least one stock for trading");
      return;
    }

    try {
      for (const stock of selectedStocks) {
        await tradingAPI.startTrading({ symbol: stock });
      }
      setTradingStarted(true);
      setTradingError("");  // ✅ Reset error if successful
    } catch (err) {
      setTradingError("Failed to start trading: " + err.message);
    }
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" align="center" gutterBottom>
          Stock Analysis & Selection
        </Typography>

        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Manual Stock Selection
          </Typography>
          <Autocomplete
            sx={{ width: 300 }}
            options={availableStocks}
            getOptionLabel={(option) => `${option.symbol} - ${option.name}`}
            onChange={(event, newValue) => handleStockSelect(newValue?.symbol)}
            renderInput={(params) => (
              <TextField {...params} label="Search and select stocks" variant="outlined" />
            )}
          />
        </Box>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Sector Analysis
        </Typography>
        <Box sx={{ display: "flex", gap: 2, alignItems: "center", mt: 2 }}>
          <Select value={sector} onChange={handleSectorChange} displayEmpty>
            <MenuItem value=""><em>All Sectors</em></MenuItem>
            <MenuItem value="Technology">Technology</MenuItem>
            <MenuItem value="Finance">Finance</MenuItem>
            <MenuItem value="Healthcare">Healthcare</MenuItem>
            <MenuItem value="Consumer">Consumer</MenuItem>
            <MenuItem value="Energy">Energy</MenuItem>
          </Select>
          <Button variant="contained" onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Stocks"}
          </Button>
        </Box>
        {loading && <Typography>Loading...</Typography>}
        {error && <Alert severity="error">{error}</Alert>}

        {analysisResult && (
          <Typography variant="h6" sx={{ mt: 2 }}>
            Analysis Results Available
          </Typography>
        )}

        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Selected Stocks for Trading
          </Typography>
          {selectedStocks.length > 0 ? (
            <>
              <Button
                variant="contained"
                color="success"
                startIcon={<PlayArrow />}
                onClick={handleStartTrading}
                disabled={tradingStarted}
              >
                {tradingStarted ? "Trading Started" : "Start Trading"}
              </Button>
            </>
          ) : (
            <Typography color="text.secondary">
              No stocks selected. Please select stocks manually or from analysis results.
            </Typography>
          )}
        </Box>

        {/* ✅ Show trading error if it exists */}
        {tradingError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {tradingError}
          </Alert>
        )}
      </Paper>
    </Container>
  );
};

export default StockAnalysisPage;
