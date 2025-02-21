import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Typography,
  CircularProgress
} from '@mui/material';
import { tradingAPI } from '../services/api';

const TradesList = ({ symbol }) => {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (symbol) {
      loadTrades();
    }
  }, [symbol]);

  const loadTrades = async () => {
    try {
      const data = await tradingAPI.getTrades(symbol);
      setTrades(data);
    } catch (error) {
      console.error('Failed to load trades:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper sx={{ mt: 3 }}>
      <Box p={2}>
        <Typography variant="h6" gutterBottom>
          Trade History - {symbol}
        </Typography>
      </Box>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell align="right">Quantity</TableCell>
              <TableCell align="right">P&L</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {trades.map((trade) => (
              <TableRow key={trade.id}>
                <TableCell>
                  {new Date(trade.created_at).toLocaleString()}
                </TableCell>
                <TableCell>
                  <Typography 
                    color={trade.trade_type === 'BUY' ? 'success.main' : 'error.main'}
                  >
                    {trade.trade_type}
                  </Typography>
                </TableCell>
                <TableCell align="right">₹{trade.entry_price}</TableCell>
                <TableCell align="right">{trade.quantity}</TableCell>
                <TableCell align="right">
                  <Typography 
                    color={trade.profit_loss >= 0 ? 'success.main' : 'error.main'}
                  >
                    ₹{trade.profit_loss || 0}
                  </Typography>
                </TableCell>
                <TableCell>{trade.status}</TableCell>
              </TableRow>
            ))}
            {trades.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  No trades found for this symbol
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default TradesList;