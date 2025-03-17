import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, CircularProgress, Modal } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import BrokerConfigCard from './BrokerConfigCard';
import apiClient from '../services/api';  // ✅ Use global Axios client
import BrokerConfigModal from './BrokerConfigModal';

const BrokerConfigList = () => {
  const [configs, setConfigs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false); // ✅ Controls the popup modal

  useEffect(() => {
    loadConfigs();
  }, []);

  const loadConfigs = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get(`/api/broker/list`); // ✅ Uses apiClient (handles 401)
      setConfigs(response.data.brokers);
    } catch (error) {
      console.error('❌ Failed to load broker configs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await apiClient.delete(`/api/broker/delete/${id}`); // ✅ Uses apiClient
      await loadConfigs();
    } catch (error) {
      console.error('❌ Failed to delete broker config:', error);
    }
  };

  const handleToggleActive = async (id) => {
    try {
      await apiClient.put(`/api/broker/toggle/${id}`, {}); // ✅ Uses apiClient
      await loadConfigs();
    } catch (error) {
      console.error('❌ Failed to toggle broker status:', error);
    }
  };

  return (
    <Box>
      {/* ✅ Header Section with Add Broker Button */}
      <Box display="flex" justifyContent="space-between" mb={3}>
        <Typography variant="h5">Broker Configurations</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setModalOpen(true)} // ✅ Opens popup modal
        >
          Add Broker
        </Button>
      </Box>

      {/* ✅ Show Loading Indicator */}
      {loading ? <CircularProgress /> : (
        <>
          {configs.length > 0 ? configs.map((config) => (
            <BrokerConfigCard
              key={config.id}
              config={config}
              onDelete={handleDelete}
              onToggleActive={handleToggleActive}
            />
          )) : (
            <Typography color="text.secondary" align="center">
              No brokers added. Click "Add Broker" to start.
            </Typography>
          )}
        </>
      )}

      {/* ✅ Broker Add/Edit Modal */}
      <Modal open={modalOpen} onClose={() => setModalOpen(false)}>
        <BrokerConfigModal open={modalOpen} onClose={() => setModalOpen(false)} refreshBrokers={loadConfigs} />
      </Modal>
    </Box>
  );
};

export default BrokerConfigList;
