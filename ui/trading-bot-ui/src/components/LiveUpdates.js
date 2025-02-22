// src/components/LiveUpdates.js
import React from "react";
import { Box, Typography, List, ListItem, ListItemText } from "@mui/material";

function LiveUpdates({ updates }) {
  return (
    <Box sx={{ p: 3, background: "#111", borderRadius: 2 }}>
      <Typography variant="h6" sx={{ mb: 2, color: "primary.main" }}>
        Live Trading Updates
      </Typography>
      <List>
        {updates.map((update, index) => (
          <ListItem key={index}>
            <ListItemText primary={update.message} secondary={update.timestamp} sx={{ color: "text.secondary" }} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

export default LiveUpdates;
