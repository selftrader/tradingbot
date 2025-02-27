import React from "react";
import { Card, CardContent, Typography } from "@mui/material";

const PortfolioTracker = () => {
  return (
    <Card sx={{ padding: 2 }}>
      <CardContent>
        <Typography variant="h6">Portfolio Performance</Typography>
        <Typography variant="body1" color="secondary">
          Total Profit/Loss: ₹ 12,500
        </Typography>
      </CardContent>
    </Card>
  );
};

export default PortfolioTracker; // ✅ Ensure default export
