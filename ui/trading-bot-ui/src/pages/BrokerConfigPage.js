import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Button,
  CircularProgress,
  Modal,
} from "@mui/material";
import BrokerConfigCard from "../components/BrokerConfigCard";
import BrokerConfigModal from "../components/settings/BrokerConfigModal";
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const BrokerConfigPage = () => {
  const [brokers, setBrokers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false); // ✅ Controls the popup modal

  // ✅ Fetch Brokers from API
  const fetchBrokers = useCallback(async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.get(`${API_URL}/api/broker/list`, { headers });
      setBrokers(response.data.brokers);
    } catch (error) {
      console.error("❌ Failed to load brokers:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBrokers();
  }, [fetchBrokers]);

  // ✅ Delete Broker Function
  const deleteBroker = async (brokerId) => {
    if (!window.confirm("Are you sure you want to remove this broker?")) return;
    
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");
      const headers = { Authorization: `Bearer ${token}` };

      await axios.delete(`${API_URL}/api/broker/delete/${brokerId}`, { headers });
      fetchBrokers();
    } catch (error) {
      console.error("❌ Failed to delete broker:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={3}>
      {/* ✅ Header with "Add Broker" Button */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">Broker Configurations</Typography>
        <Button variant="contained" onClick={() => setModalOpen(true)}>
          Add Broker
        </Button>
      </Box>

      {/* ✅ Loading Indicator */}
      {loading ? <CircularProgress /> : (
        <>
          {brokers.length > 0 ? brokers.map((broker) => (
            <BrokerConfigCard
              key={broker.id}
              config={broker}
              onDelete={deleteBroker}
            />
          )) : (
            <Typography color="text.secondary" align="center">
              No brokers added. Click "Add Broker" to start.
            </Typography>
          )}
        </>
      )}

      {/* ✅ Add Broker Popup Modal */}
      <Modal open={modalOpen} onClose={() => setModalOpen(false)}>
        <BrokerConfigModal open={modalOpen} onClose={() => setModalOpen(false)} refreshBrokers={fetchBrokers} />
      </Modal>
    </Box>
  );
};

export default BrokerConfigPage;
