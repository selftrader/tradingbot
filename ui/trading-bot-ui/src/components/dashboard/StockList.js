// src/components/Dashboard/StockList.js

import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  CircularProgress,
} from "@mui/material";
import axios from "axios";

const StockList = () => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("/api/dashboard/stocks")
      .then((res) => {
        setStocks(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching stock list:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" my={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box mt={4}>
      <Typography variant="h6" gutterBottom>
        📊 Tracked Stocks (F&O)
      </Typography>
      <Paper elevation={2}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Symbol</TableCell>
              <TableCell>Company Name</TableCell>
              <TableCell>Exchange</TableCell>
              <TableCell>ATM Strike</TableCell>
              <TableCell>Expiry</TableCell>
              <TableCell>Strike Range</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {stocks.map((stock, index) => (
              <TableRow key={index}>
                <TableCell>{stock.symbol}</TableCell>
                <TableCell>{stock.name}</TableCell>
                <TableCell>{stock.exchange}</TableCell>
                <TableCell>{stock.atm}</TableCell>
                <TableCell>{stock.expiry}</TableCell>
                <TableCell>{stock.strike_prices.join(", ")}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
};

export default StockList;
