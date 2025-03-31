import React, { useState, useEffect } from "react";
import {
  TextField,
  MenuItem,
  Button,
  Grid,
  Autocomplete,
  CircularProgress,
} from "@mui/material";
import { fetchStockList,resolveStockDetails } from "../../services/marketDataService";

const StockSearch = ({ onSearch }) => {
  const [exchange, setExchange] = useState("NSE");
  const [instrument, setInstrument] = useState("Equity");
  const [stockOptions, setStockOptions] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchStocks = async () => {
      setLoading(true);
      try {
        const stocks = await fetchStockList(exchange, instrument);
        setStockOptions(stocks || []);
      } catch (error) {
        console.error("Error fetching stocks", error);
      }
      setLoading(false);
    };
    fetchStocks();
  }, [exchange, instrument]);

  const handleSearch = async () => {
    if (!selectedStock || !selectedStock.symbol) return;
  
    try {
      const fullStock = await resolveStockDetails(selectedStock.symbol, exchange);
  
      if (fullStock) {
        onSearch(fullStock); // Pass enriched stock object
        setSelectedStock(null);
      }
    } catch (err) {
      console.error("Error in stock resolve", err);
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={6} md={3}>
        <TextField
          select
          label="Exchange"
          value={exchange}
          fullWidth
          onChange={(e) => setExchange(e.target.value)}
        >
          <MenuItem value="NSE">NSE</MenuItem>
          <MenuItem value="BSE">BSE</MenuItem>
          <MenuItem value="MCX">MCX</MenuItem>
        </TextField>
      </Grid>

      <Grid item xs={6} md={3}>
        <TextField
          select
          label="Instrument"
          value={instrument}
          fullWidth
          onChange={(e) => setInstrument(e.target.value)}
        >
          <MenuItem value="Equity">Equity</MenuItem>
          <MenuItem value="Futures">Futures</MenuItem>
          <MenuItem value="Options">Options</MenuItem>
        </TextField>
      </Grid>

      <Grid item xs={12} md={4}>
        <Autocomplete
          options={stockOptions}
          getOptionLabel={(option) =>
            `${option.symbol} - ${option.name || ""} (${option.instrument_type || ""})`
          }
          value={selectedStock}
          onChange={(event, newValue) => setSelectedStock(newValue)}
          isOptionEqualToValue={(option, value) =>
            option.instrumentKey === value?.instrumentKey
          }
          renderInput={(params) => (
            <TextField
              {...params}
              label="Search Stock"
              variant="outlined"
              fullWidth
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <>
                    {loading && <CircularProgress size={20} />}
                    {params.InputProps.endAdornment}
                  </>
                ),
              }}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={2}>
        <Button
          variant="contained"
          fullWidth
          onClick={handleSearch}
          disabled={!selectedStock}
        >
          Add Stock
        </Button>
      </Grid>
    </Grid>
  );
};

export default StockSearch;
