import React, { useState, useEffect } from 'react';
import {
  Button,
  Stack,
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import { PlayArrow, Stop, Settings } from '@mui/icons-material';
import { tradingAPI } from '../services/api';

const TradeControlButtons = ({ socket }) => {
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [availableStocks, setAvailableStocks] = useState([]);
  const [botStatus, setBotStatus] = useState('idle');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch available stocks on component mount
  useEffect(() => {
    fetchAvailableStocks();
  }, []);

  // Socket event listeners
  useEffect(() => {
    if (!socket) return;

    socket.on('bot_status', (status) => {
      setBotStatus(status);
      setLoading(false);
    });

    socket.on('error', (error) => {
      setError(error.message);
      setLoading(false);
    });

    return () => {
      socket.off('bot_status');
      socket.off('error');
    };
  }, [socket]);

  const fetchAvailableStocks = async () => {
    try {
      const stocks = await tradingAPI.getAvailableStocks();
      setAvailableStocks(stocks);
    } catch (err) {
      setError('Failed to fetch available stocks');
    }
  };

  const startTrade = async () => {
    if (selectedStocks.length === 0) {
      setError('Please select at least one stock');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const response = await tradingAPI.startBot(selectedStocks);

      if (response.success) {
        setBotStatus('running');
        socket.emit('start_trading', { symbols: selectedStocks });
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to start trading');
      setBotStatus('idle');
    } finally {
      setLoading(false);
    }
  };

  const stopTrade = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await tradingAPI.stopBot();
      
      if (response.success) {
        setBotStatus('stopped');
        socket.emit('stop_trading');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to stop trading');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Trading Bot Control
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Select Stocks</InputLabel>
        <Select
          multiple
          value={selectedStocks}
          onChange={(e) => setSelectedStocks(e.target.value)}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          disabled={botStatus === 'running' || loading}
        >
          {availableStocks.map((stock) => (
            <MenuItem key={stock.symbol} value={stock.symbol}>
              {stock.symbol} - {stock.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Stack spacing={2} direction="row" alignItems="center">
        <Button
          variant="contained"
          color="success"
          startIcon={<PlayArrow />}
          onClick={startTrade}
          disabled={botStatus === 'running' || loading || selectedStocks.length === 0}
        >
          Start Bot
        </Button>

        <Button
          variant="contained"
          color="error"
          startIcon={<Stop />}
          onClick={stopTrade}
          disabled={botStatus !== 'running' || loading}
        >
          Stop Bot
        </Button>

        <Button
          variant="outlined"
          startIcon={<Settings />}
          onClick={() => {/* Add settings dialog */}}
        >
          Settings
        </Button>

        {loading && <CircularProgress size={24} />}

        <Chip
          label={`Status: ${botStatus.toUpperCase()}`}
          color={
            botStatus === 'running' ? 'success' :
            botStatus === 'stopped' ? 'error' :
            'default'
          }
        />
      </Stack>
    </Box>
  );
};

export default TradeControlButtons;
