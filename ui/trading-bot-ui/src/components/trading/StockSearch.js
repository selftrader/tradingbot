import React, { useState, useEffect } from "react";
import { TextField, MenuItem, Button, Grid, Autocomplete, CircularProgress } from "@mui/material";
import { fetchStockList } from "../../services/marketDataService";

const StockSearch = ({ onSearch }) => {
  const [exchange, setExchange] = useState("NSE");
  const [instrument, setInstrument] = useState("Equity");
  const [stockSymbol, setStockSymbol] = useState("");
  const [stockOptions, setStockOptions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchStocks = async () => {
      setLoading(true);
      const stocks = await fetchStockList(exchange, instrument);
      setStockOptions(stocks || []);
      setLoading(false);
    };
    fetchStocks();
  }, [exchange, instrument]);

  const handleSearch = () => {
    if (stockSymbol) {
      onSearch(stockSymbol, exchange, instrument);
      setStockSymbol(""); 
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={6} md={3}>
        <TextField select label="Exchange" value={exchange} fullWidth onChange={(e) => setExchange(e.target.value)}>
          <MenuItem value="NSE">NSE</MenuItem>
          <MenuItem value="BSE">BSE</MenuItem>
          <MenuItem value="MCX">MCX</MenuItem>
        </TextField>
      </Grid>
      <Grid item xs={6} md={3}>
        <TextField select label="Instrument" value={instrument} fullWidth onChange={(e) => setInstrument(e.target.value)}>
          <MenuItem value="Equity">Equity</MenuItem>
          <MenuItem value="Futures">Futures</MenuItem>
          <MenuItem value="Options">Options</MenuItem>
        </TextField>
      </Grid>
      <Grid item xs={12} md={4}>
        <Autocomplete
          options={stockOptions}
          getOptionLabel={(option) => option.symbol || "Unknown Stock"}
          value={stockOptions.find((stock) => stock.symbol === stockSymbol) || null}
          onChange={(event, newValue) => setStockSymbol(newValue ? newValue.symbol : "")}
          renderInput={(params) => (
            <TextField {...params} label="Search Stock" variant="outlined" fullWidth
              InputProps={{ ...params.InputProps, endAdornment: loading ? <CircularProgress size={20} /> : null }}
            />
          )}
        />
      </Grid>
      <Grid item xs={12} md={2}>
        <Button variant="contained" fullWidth onClick={handleSearch} disabled={!stockSymbol}>
          Add Stock
        </Button>
      </Grid>
    </Grid>
  );
};

export default StockSearch;
