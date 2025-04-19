import { Autocomplete, TextField, CircularProgress } from "@mui/material";
import { useState, useEffect } from "react";
import axios from "axios";

const REACT_APP_API_URL = process.env.REACT_APP_API_URL;

export default function StockOptionSearchPanel({ onOptionSelect }) {
  const [query, setQuery] = useState("");
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      if (query.length >= 2) {
        setLoading(true);
        axios
          .get(`${REACT_APP_API_URL}/api/instruments/search?q=${query}`)
          .then((res) => setOptions(res.data || []))
          .catch(console.error)
          .finally(() => setLoading(false));
      }
    }, 300);
    return () => clearTimeout(delayDebounce);
  }, [query]);

  return (
    <Autocomplete
      fullWidth
      loading={loading}
      options={options}
      getOptionLabel={(option) => `${option.symbol} - ${option.trading_symbol}`}
      onInputChange={(e, val) => setQuery(val)}
      onChange={(e, val) => onOptionSelect(val)}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Search Stock/Option"
          variant="outlined"
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
  );
}
