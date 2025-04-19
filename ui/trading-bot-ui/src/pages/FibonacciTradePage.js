import React, { useState } from "react";
import {
  Container,
  Typography,
  Select,
  MenuItem,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Box,
} from "@mui/material";
import axios from "axios";
import TradingChart from "../components/TradingChart";

const FibonacciTradePage = () => {
  const [symbol, setSymbol] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const stocks = ["HDFCBANK.NS", "RELIANCE.NS", "TCS.NS"];

  const runFibStrategy = async () => {
    if (!symbol) return;
    setLoading(true);
    try {
      const res = await axios.post(`/api/fib-trade-run?symbol=${symbol}`);
      setResult(res.data);
    } catch (e) {
      console.error("Fibonacci strategy failed:", e);
    }
    setLoading(false);
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Fibonacci AI Paper Trading
      </Typography>

      <Select
        fullWidth
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        displayEmpty
        sx={{ mt: 2 }}
      >
        <MenuItem value="" disabled>
          Select a stock
        </MenuItem>
        {stocks.map((stock) => (
          <MenuItem key={stock} value={stock}>
            {stock}
          </MenuItem>
        ))}
      </Select>

      <Button
        variant="contained"
        fullWidth
        sx={{ mt: 2 }}
        onClick={runFibStrategy}
        disabled={loading || !symbol}
      >
        {loading ? "Running..." : "Run Fibonacci Trade"}
      </Button>

      {result && (
        <>
          <Box mt={4}>
            <Typography variant="h6">
              Total P&L: ₹{result.pnl.toFixed(2)}
            </Typography>
            <Typography variant="subtitle1">
              Total Trades: {result.trades.length}
            </Typography>
          </Box>

          <Box mt={4}>
            <TradingChart
              candles={result.candles}
              trades={result.trades}
              fibLevels={result.fibonacci_levels}
            />
          </Box>

          <Box mt={4}>
            <Typography variant="h6">Trade Log</Typography>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Time</TableCell>
                  <TableCell>Signal</TableCell>
                  <TableCell>Price</TableCell>
                  <TableCell>Action</TableCell>
                  <TableCell>Quantity</TableCell>
                  <TableCell>P&L</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {result.trades.map((t, i) => (
                  <TableRow key={i}>
                    <TableCell>{t.timestamp}</TableCell>
                    <TableCell>{t.type}</TableCell>
                    <TableCell>{t.price}</TableCell>
                    <TableCell>{t.action}</TableCell>
                    <TableCell>{t.quantity}</TableCell>
                    <TableCell>
                      {t.pnl ? `₹${t.pnl.toFixed(2)}` : "-"}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Box>
        </>
      )}
    </Container>
  );
};

export default FibonacciTradePage;
