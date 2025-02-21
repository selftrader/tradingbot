import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, CircularProgress } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import BrokerConfigCard from './BrokerConfigCard';
import { tradingAPI } from '../services/api';

const BrokerConfigList = () => {
  const [configs, setConfigs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConfigs();
  }, []);

  const loadConfigs = async () => {
    try {
      const data = await tradingAPI.getBrokerConfigs();
      setConfigs(data);
    } catch (error) {
      console.error('Failed to load broker configs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async (id) => {
    // Implement edit logic
  };

  const handleDelete = async (id) => {
    try {
      await tradingAPI.deleteBrokerConfig(id);
      await loadConfigs();
    } catch (error) {
      console.error('Failed to delete broker config:', error);
    }
  };

  const handleToggleActive = async (id) => {
    try {
      await tradingAPI.toggleBrokerActive(id);
      await loadConfigs();
    } catch (error) {
      console.error('Failed to toggle broker status:', error);
    }
  };

  if (loading) return <CircularProgress />;

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" mb={3}>
        <Typography variant="h5">Broker Configurations</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleEdit(null)}
        >
          Add Broker
        </Button>
      </Box>

      {configs.map((config) => (
        <BrokerConfigCard
          key={config.id}
          config={config}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onToggleActive={handleToggleActive}
        />
      ))}

      {configs.length === 0 && (
        <Typography color="text.secondary" align="center">
          No broker configurations found. Add one to start trading.
        </Typography>
      )}
    </Box>
  );
};

export default BrokerConfigList;