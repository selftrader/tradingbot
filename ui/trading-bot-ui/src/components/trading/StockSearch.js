import React, { useState, useEffect } from "react";
import { TextField, Button, Box, MenuItem, Select, Autocomplete } from "@mui/material";
import { fetchStockList } from "../../services/stockDataService";

const StockSearch = ({ onSearch }) => {
  const [symbol, setSymbol] = useState("");
  const [exchange, setExchange] = useState("NSE"); // Default to NSE
  const [stockList, setStockList] = useState([]);

  useEffect(() => {
    const loadStockList = async () => {
      const stocks = await fetchStockList(exchange);
      setStockList(stocks);
    };
    loadStockList();
  }, [exchange]);

  const handleSearch = () => {
    if (symbol.trim()) {
      onSearch({ symbol: symbol.toUpperCase(), exchange });
    }
  };

  return (
    <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", mt: 4 }}>
      <Select
        value={exchange}
        onChange={(e) => setExchange(e.target.value)}
        sx={{ width: 120, mr: 2 }}
      >
        <MenuItem value="NSE">NSE</MenuItem>
        <MenuItem value="BSE">BSE</MenuItem>
      </Select>

      <Autocomplete
        options={stockList}
        getOptionLabel={(option) => option.symbol}
        onChange={(event, newValue) => setSymbol(newValue ? newValue.symbol : "")}
        renderInput={(params) => (
          <TextField {...params} label="Search Stock" variant="outlined" sx={{ width: "250px", mr: 2 }} />
        )}
      />

      <Button
        variant="contained"
        sx={{ backgroundColor: "#ff44ff", color: "black", borderRadius: "20px" }}
        onClick={handleSearch}
      >
        Search
      </Button>
    </Box>
  );
};

export default StockSearch;
