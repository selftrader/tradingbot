// src/pages/OptionChainPage.jsx
import {
  Box,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  ToggleButtonGroup,
  ToggleButton,
  Chip,
  Divider,
} from "@mui/material";
import { useParams } from "react-router-dom";
import { useMarket } from "../context/MarketProvider";
import { useState } from "react";

const format = (val, dec = 2) => (val == null ? "–" : Number(val).toFixed(dec));

const OptionChainPage = () => {
  const { symbol } = useParams();
  const { groupedStocks, ltps } = useMarket();

  const stock = groupedStocks[symbol?.toUpperCase()];
  const [expiry, setExpiry] = useState("24 APR"); // Default expiry

  if (!stock) {
    return <Typography>❌ Stock not found</Typography>;
  }

  const getLTP = (key) => ltps[key?.toUpperCase()]?.ltp ?? null;

  const spot = stock.spot;
  const spotLTP = getLTP(spot.instrument_key);
  const lotSize = spot.lot_size;

  // Group options by strike
  const strikeMap = {};
  [...(stock.options.call || []), ...(stock.options.put || [])].forEach(
    (opt) => {
      if (!opt.expiry) return;
      const expiryLabel = new Date(opt.expiry).toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
      });
      if (expiryLabel !== expiry) return;

      if (!strikeMap[opt.strike_price]) strikeMap[opt.strike_price] = {};
      if (opt.option_type === "CE") strikeMap[opt.strike_price].ce = opt;
      if (opt.option_type === "PE") strikeMap[opt.strike_price].pe = opt;
    }
  );

  const rows = Object.entries(strikeMap)
    .map(([strike, data]) => ({ strike: Number(strike), ...data }))
    .sort((a, b) => a.strike - b.strike);

  const expiries = Array.from(
    new Set([
      ...stock.options.call.map((o) =>
        new Date(o.expiry).toLocaleDateString("en-IN", {
          day: "2-digit",
          month: "short",
        })
      ),
      ...stock.options.put.map((o) =>
        new Date(o.expiry).toLocaleDateString("en-IN", {
          day: "2-digit",
          month: "short",
        })
      ),
    ])
  );

  return (
    <Box p={3}>
      <Typography variant="h5" mb={1}>
        {symbol} Option Chain
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={2}>
        Spot LTP: ₹{format(spotLTP)} | Lot Size: {lotSize}
      </Typography>

      <ToggleButtonGroup
        value={expiry}
        exclusive
        onChange={(e, val) => val && setExpiry(val)}
        sx={{ mb: 2 }}
      >
        {expiries.map((exp) => (
          <ToggleButton key={exp} value={exp}>
            {exp}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>

      <Chip
        label={`Synthetic FUT ${format(spotLTP)}`}
        variant="outlined"
        color="primary"
        sx={{ mb: 2, ml: 2 }}
      />

      <Divider sx={{ my: 2 }} />

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell align="right">Δ</TableCell>
            <TableCell align="right">Call LTP</TableCell>
            <TableCell align="right">Lots</TableCell>
            <TableCell align="center">Strike</TableCell>
            <TableCell align="left">IV</TableCell>
            <TableCell align="left">Lots</TableCell>
            <TableCell align="left">Put LTP</TableCell>
            <TableCell align="left">Δ</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => {
            const ce = row.ce || {};
            const pe = row.pe || {};
            const callLTP = getLTP(ce.instrument_key);
            const putLTP = getLTP(pe.instrument_key);
            const isATM = Math.abs(row.strike - spotLTP) < 5;

            return (
              <TableRow
                key={row.strike}
                sx={{ bgcolor: isATM ? "#e3f2fd" : "inherit" }}
              >
                <TableCell align="right">{format(ce.delta)}</TableCell>
                <TableCell align="right">{format(callLTP)}</TableCell>
                <TableCell align="right">{ce.lot_size ?? "–"}</TableCell>
                <TableCell align="center">
                  <strong>{row.strike}</strong>
                </TableCell>
                <TableCell align="left">{format(pe.iv)}</TableCell>
                <TableCell align="left">{pe.lot_size ?? "–"}</TableCell>
                <TableCell align="left">{format(putLTP)}</TableCell>
                <TableCell align="left">{format(pe.delta)}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </Box>
  );
};

export default OptionChainPage;
