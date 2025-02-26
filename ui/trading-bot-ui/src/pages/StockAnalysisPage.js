//// filepath: /c:/Work/P/app/tradingapp-main/tradingapp-main/ui/trading-bot-ui/src/pages/StockAnalysisPage.js
import React, { useState, useEffect } from 'react';
import { analyzeSectoralOptions, tradingAPI } from "../services/api";
import {
    Container,
    Paper,
    Typography,
    FormControl,
    Select,
    MenuItem,
    Box,
    Button,
    Table,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Checkbox,
    Chip,
    Alert,
    Autocomplete,
    TextField,
    Divider
} from '@mui/material';
import { PlayArrow } from '@mui/icons-material';

const StockAnalysisPage = () => {
  const [sector, setSector] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  // const [analysis, setAnalysis] = useState(null);
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [tradingStarted, setTradingStarted] = useState(false);
  const [tradingError, setTradingError] = useState("");
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
    setLoading(true);
    setError("");
    try {
      const result = await analyzeSectoralOptions();
      setAnalysisResult(result);
    } catch (err) {
      setError("Analysis failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // const fetchAnalysis = async (sector) => {
  //   try {
  //     const data = await analyzeSectoralOptions(sector);
  //     setAnalysis(data);
  //   } catch (error) {
  //     console.error('Error fetching analysis:', error);
  //   }
  // };

  const handleStockSelect = (stock) => {
    setSelectedStocks(prev => 
      prev.includes(stock) 
        ? prev.filter(s => s !== stock)
        : [...prev, stock]
    );
  };

  const handleManualStockSelect = (event, newValue) => {
    if (newValue && !selectedStocks.includes(newValue.symbol)) {
      setSelectedStocks(prev => [...prev, newValue.symbol]);
    }
  };

  const handleStartTrading = async () => {
    if (selectedStocks.length === 0) {
      setTradingError("Please select at least one stock for trading");
      return;
    }

    try {
      await tradingAPI.startTrading(selectedStocks);
      setTradingStarted(true);
      setTradingError("");
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

        {/* Manual Stock Selection Section */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Manual Stock Selection
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <Autocomplete
              sx={{ width: 300 }}
              options={availableStocks}
              getOptionLabel={(option) => `${option.symbol} - ${option.name}`}
              onChange={handleManualStockSelect}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Search and select stocks"
                  variant="outlined"
                />
              )}
            />
          </Box>
        </Box>

        <Divider sx={{ my: 3 }} />

        {/* Sector Analysis Section */}
        <Typography variant="h6" gutterBottom>
          Sector Analysis
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mt: 2 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <Select
              value={sector}
              onChange={handleSectorChange}
              displayEmpty
            >
              <MenuItem value="">
                <em>All Sectors</em>
              </MenuItem>
              <MenuItem value="Technology">Technology</MenuItem>
              <MenuItem value="Finance">Finance</MenuItem>
              <MenuItem value="Healthcare">Healthcare</MenuItem>
              <MenuItem value="Consumer">Consumer</MenuItem>
              <MenuItem value="Energy">Energy</MenuItem>
            </Select>
          </FormControl>
          <Button variant="contained" onClick={handleAnalyze}>
            {loading ? "Analyzing..." : "Analyze Stocks"}
          </Button>
        </Box>
        {error && <Typography color="error">{error}</Typography>}
        {analysisResult && analysisResult.recommendedStocks && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Recommended Stocks
            </Typography>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Select</TableCell>
                  <TableCell>Symbol</TableCell>
                  <TableCell>Sector</TableCell>
                  <TableCell>Confidence</TableCell>
                  <TableCell>Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {analysisResult.recommendedStocks.map((stock, index) => (
                  <TableRow 
                    key={index}
                    sx={{
                      backgroundColor: selectedStocks.includes(stock.symbol) 
                        ? 'action.selected' 
                        : 'inherit'
                    }}
                  >
                    <TableCell>
                      <Checkbox
                        checked={selectedStocks.includes(stock.symbol)}
                        onChange={() => handleStockSelect(stock.symbol)}
                      />
                    </TableCell>
                    <TableCell>{stock.symbol}</TableCell>
                    <TableCell>{stock.sector}</TableCell>
                    <TableCell>
                      <Chip 
                        label={`${(stock.confidence * 100).toFixed(1)}%`}
                        color={stock.confidence > 0.7 ? "success" : "warning"}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={stock.action}
                        color={stock.action === 'BUY' ? 'success' : 'error'}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Box>
        )}

        {/* Selected Stocks Section - Move outside of analysisResult condition */}
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Selected Stocks for Trading
          </Typography>
          {selectedStocks.length > 0 ? (
            <>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                {selectedStocks.map(stock => (
                  <Chip
                    key={stock}
                    label={stock}
                    onDelete={() => handleStockSelect(stock)}
                    color="primary"
                    size="small"
                  />
                ))}
              </Box>
              <Button
                variant="contained"
                color="success"
                startIcon={<PlayArrow />}
                onClick={handleStartTrading}
                disabled={tradingStarted}
              >
                {tradingStarted ? 'Trading Started' : 'Start Trading'}
              </Button>
            </>
          ) : (
            <Typography color="text.secondary">
              No stocks selected. Please select stocks manually or from analysis results.
            </Typography>
          )}
        </Box>

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