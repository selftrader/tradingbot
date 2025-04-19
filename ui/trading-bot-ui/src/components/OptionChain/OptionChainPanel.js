// src/components/OptionChain/OptionChainPanel.jsx
import {
  Box,
  Grid,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  ToggleButton,
  ToggleButtonGroup,
  CircularProgress,
  Chip,
} from "@mui/material";
import { useEffect, useState } from "react";
import axios from "axios";

const expiries = ["24 APR", "29 MAY", "26 JUN", "25 SEP"];

const OptionChainPanel = () => {
  const [symbol, setSymbol] = useState("BANKNIFTY"); // default
  const [expiry, setExpiry] = useState(expiries[0]);
  const [chainData, setChainData] = useState([]);
  const [atmStrike, setAtmStrike] = useState(null);
  const [loading, setLoading] = useState(false);
  const lotSize = 30; // example

  const fetchOptionChain = async () => {
    setLoading(true);
    try {
      const res = await axios.get(
        `/api/options/chain?symbol=${symbol}&expiry=${expiry}`
      );
      setChainData(res.data.chain || []);
      setAtmStrike(res.data.atm || null);
    } catch (err) {
      console.error("Error fetching chain", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchOptionChain();
  }, [expiry]);

  const isATM = (strike) => Number(strike) === Number(atmStrike);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Option Chain – {symbol} (Lot size: {lotSize})
      </Typography>

      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <Box display="flex" gap={2}>
          {expiries.map((ex) => (
            <Button
              key={ex}
              variant={ex === expiry ? "contained" : "outlined"}
              onClick={() => setExpiry(ex)}
            >
              {ex}
            </Button>
          ))}
        </Box>
        <Chip
          label={`Synthetic FUT ${atmStrike}`}
          color="info"
          variant="outlined"
        />
      </Box>

      {loading ? (
        <CircularProgress />
      ) : (
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Delta</TableCell>
              <TableCell>Call LTP</TableCell>
              <TableCell>Lots</TableCell>
              <TableCell>Strike</TableCell>
              <TableCell>IV</TableCell>
              <TableCell>Lots</TableCell>
              <TableCell>Put LTP</TableCell>
              <TableCell>Delta</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {chainData.map((row, i) => {
              const strike = row.strike_price;
              const atm = isATM(strike);
              return (
                <TableRow
                  key={i}
                  style={{
                    backgroundColor: atm
                      ? "#e3f2fd"
                      : i % 2 === 0
                      ? "#fff"
                      : "#f9f9f9",
                  }}
                >
                  <TableCell>{row.ce?.delta?.toFixed(2) ?? "–"}</TableCell>
                  <TableCell>{row.ce?.ltp?.toFixed(2) ?? "–"}</TableCell>
                  <TableCell>{row.ce?.lots ?? "–"}</TableCell>
                  <TableCell style={{ fontWeight: atm ? 600 : 400 }}>
                    {strike}
                  </TableCell>
                  <TableCell>{row.ce?.iv?.toFixed(1) ?? "–"}</TableCell>
                  <TableCell>{row.pe?.lots ?? "–"}</TableCell>
                  <TableCell>{row.pe?.ltp?.toFixed(2) ?? "–"}</TableCell>
                  <TableCell>{row.pe?.delta?.toFixed(2) ?? "–"}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      )}
    </Box>
  );
};

export default OptionChainPanel;
