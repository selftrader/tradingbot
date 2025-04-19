import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Select,
  MenuItem,
  Button,
  Box,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TextField,
  Grid,
  FormControl,
  InputLabel,
} from "@mui/material";
import axios from "axios";
import StockOptionSearchPanel from "../components/StockOptionSearchPanel";
import StrikeRangeSelector from "../components/StrikeRangeSelector";
import OptionChainTable from "../components/OptionChain//OptionChainTable";

const PaperTradingPage = () => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [strategy, setStrategy] = useState("rsi");
  const [capital, setCapital] = useState("10000");
  const [stopLoss, setStopLoss] = useState("2");
  const [target, setTarget] = useState("4");
  const [timeframe, setTimeframe] = useState("5m");
  const [mode, setMode] = useState("paper");
  const [strikeRange, setStrikeRange] = useState(20);
  const [chainData, setChainData] = useState(null);
  const [summary, setSummary] = useState(null);
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedOption?.symbol) {
      axios
        .get(
          `${process.env.REACT_APP_API_URL}/api/instruments/chain?symbol=${selectedOption.symbol}&range=${strikeRange}`
        )
        .then((res) => setChainData(res.data))
        .catch(console.error);
    }
  }, [selectedOption, strikeRange]);

  const handleStart = async () => {
    if (!selectedOption?.instrument_key)
      return alert("Select an option first!");
    setLoading(true);
    try {
      const res = await axios.post(`/api/paper-trade`, {
        instrument_key: selectedOption.instrument_key,
        strategy,
        capital,
        stopLoss,
        target,
        timeframe,
        mode,
      });
      setSummary(res.data);
      setTrades(res.data.trades);
    } catch (err) {
      console.error("Paper trade failed:", err);
    }
    setLoading(false);
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        AI Paper Trading
      </Typography>
      <Box mt={3} mb={2}>
        <StockOptionSearchPanel onOptionSelect={setSelectedOption} />
      </Box>

      {selectedOption && (
        <Box mt={2}>
          <Typography variant="h6">📄 Selected Option</Typography>
          <Typography>Symbol: {selectedOption.trading_symbol}</Typography>
          <Typography>Strike: ₹{selectedOption.strike_price}</Typography>
          <Typography>Expiry: {selectedOption.expiry}</Typography>
          <Typography>Option Type: {selectedOption.option_type}</Typography>
          <Typography>
            Instrument Key: {selectedOption.instrument_key}
          </Typography>
        </Box>
      )}

      <Grid container spacing={2} mt={2}>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="Capital (₹)"
            value={capital}
            onChange={(e) => setCapital(e.target.value)}
          />
        </Grid>
        <Grid item xs={6}>
          <FormControl fullWidth>
            <InputLabel>Strategy</InputLabel>
            <Select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
            >
              <MenuItem value="rsi">RSI</MenuItem>
              <MenuItem value="ema">EMA Crossover</MenuItem>
              <MenuItem value="fibonacci">Fibonacci</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="Stop Loss %"
            value={stopLoss}
            onChange={(e) => setStopLoss(e.target.value)}
          />
        </Grid>
        <Grid item xs={6}>
          <TextField
            fullWidth
            label="Target %"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
          />
        </Grid>
        <Grid item xs={6}>
          <FormControl fullWidth>
            <InputLabel>Timeframe</InputLabel>
            <Select
              value={timeframe}
              onChange={(e) => setTimeframe(e.target.value)}
            >
              <MenuItem value="1m">1 Min</MenuItem>
              <MenuItem value="5m">5 Min</MenuItem>
              <MenuItem value="15m">15 Min</MenuItem>
              <MenuItem value="1d">Daily</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6}>
          <FormControl fullWidth>
            <InputLabel>Mode</InputLabel>
            <Select value={mode} onChange={(e) => setMode(e.target.value)}>
              <MenuItem value="paper">Paper</MenuItem>
              <MenuItem value="live">Live</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <StrikeRangeSelector value={strikeRange} onChange={setStrikeRange} />
        </Grid>
      </Grid>

      <Box mt={3}>
        <Button
          variant="contained"
          fullWidth
          onClick={handleStart}
          disabled={!selectedOption || loading}
        >
          {loading ? "Running..." : "Start Paper Trade"}
        </Button>
      </Box>

      <OptionChainTable chainData={chainData} />

      {summary && (
        <Box mt={4}>
          <Typography variant="h6">📈 Summary</Typography>
          <Typography>Total Trades: {summary.total_trades}</Typography>
          <Typography>Total P&L: ₹{summary.pnl.toFixed(2)}</Typography>
          <Typography>
            Profit %: {summary.profit_percent.toFixed(2)}%
          </Typography>
        </Box>
      )}

      {trades.length > 0 && (
        <Box mt={4}>
          <Typography variant="h6">📋 Trade Log</Typography>
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
              {trades.map((t, i) => (
                <TableRow key={i}>
                  <TableCell>{t.timestamp}</TableCell>
                  <TableCell>{t.type}</TableCell>
                  <TableCell>{t.price}</TableCell>
                  <TableCell>{t.action}</TableCell>
                  <TableCell>{t.quantity}</TableCell>
                  <TableCell>{t.pnl ? `₹${t.pnl.toFixed(2)}` : "-"}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      )}
    </Container>
  );
};

export default PaperTradingPage;
