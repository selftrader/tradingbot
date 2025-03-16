import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, CircularProgress, Modal } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import BrokerConfigCard from './BrokerConfigCard';
import axios from 'axios';
import BrokerConfigModal from './BrokerConfigModal';

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

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
      const token = localStorage.getItem("accessToken");
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.get(`${API_URL}/api/broker/list`, { headers });
      setConfigs(response.data.brokers);
    } catch (error) {
      console.error('❌ Failed to load broker configs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      const token = localStorage.getItem("accessToken");
      const headers = { Authorization: `Bearer ${token}` };

      await axios.delete(`${API_URL}/api/broker/delete/${id}`, { headers });
      await loadConfigs();
    } catch (error) {
      console.error('❌ Failed to delete broker config:', error);
    }
  };

  const handleToggleActive = async (id) => {
    try {
      const token = localStorage.getItem("accessToken");
      const headers = { Authorization: `Bearer ${token}` };

      await axios.put(`${API_URL}/api/broker/toggle/${id}`, {}, { headers });
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
