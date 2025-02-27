import React, { useState, useEffect } from "react";
import { Modal, Box, Typography, TextField, Button, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

const TradeSettingsModal = ({ open, onClose, stock, setSelectedStocks }) => {
  const [settings, setSettings] = useState({ target: "", stopLoss: "", amount: "" });

  // ✅ Load existing stock settings when modal opens
  useEffect(() => {
    if (stock) {
      setSettings({
        target: stock.target || "",
        stopLoss: stock.stopLoss || "",
        amount: stock.amount || "",
      });
    }
  }, [stock]);

  // ✅ Update stock settings in the main list
  const handleSave = () => {
    if (!stock) return;
    setSelectedStocks(prevStocks =>
      prevStocks.map(s => (s.symbol === stock.symbol ? { ...s, ...settings } : s))
    );
    onClose(); // ✅ Close modal after saving
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          width: 400,
          p: 3,
          backgroundColor: "white",
          borderRadius: "8px",
          mx: "auto",
          mt: "20vh",
          position: "relative",
          boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
        }}
      >
        {/* ✅ Close Button */}
        <IconButton
          onClick={onClose}
          sx={{ position: "absolute", top: 8, right: 8, color: "#555" }}
        >
          <CloseIcon />
        </IconButton>

        {/* ✅ Modal Header */}
        <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2 }}>
          Trade Settings for {stock?.symbol || "Unknown"}
        </Typography>

        {/* ✅ Target Price */}
        <TextField
          fullWidth
          label="Target Price (₹)"
          margin="normal"
          type="number"
          value={settings.target}
          onChange={(e) => setSettings({ ...settings, target: e.target.value })}
        />

        {/* ✅ Stop Loss */}
        <TextField
          fullWidth
          label="Stop Loss (₹)"
          margin="normal"
          type="number"
          value={settings.stopLoss}
          onChange={(e) => setSettings({ ...settings, stopLoss: e.target.value })}
        />

        {/* ✅ Investment Amount */}
        <TextField
          fullWidth
          label="Investment Amount (₹)"
          margin="normal"
          type="number"
          value={settings.amount}
          onChange={(e) => setSettings({ ...settings, amount: e.target.value })}
        />

        {/* ✅ Save Button */}
        <Button
          fullWidth
          variant="contained"
          color="primary"
          sx={{ mt: 2, fontWeight: "bold" }}
          onClick={handleSave}
        >
          Save
        </Button>
      </Box>
    </Modal>
  );
};

export default TradeSettingsModal;
