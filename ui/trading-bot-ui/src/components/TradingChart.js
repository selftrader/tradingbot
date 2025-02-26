import React, { useEffect, useRef } from "react";
import { Box, Typography } from "@mui/material";
import { createChart } from "lightweight-charts";

const TradingChart = () => {
  const chartContainerRef = useRef(null);

  useEffect(() => {
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 300,
      layout: { backgroundColor: "#1e1e1e", textColor: "#fff" },
      grid: { vertLines: { color: "#333" }, horzLines: { color: "#333" } },
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderUpColor: "#26a69a",
      borderDownColor: "#ef5350",
      wickUpColor: "#26a69a",
      wickDownColor: "#ef5350",
    });

    // Simulated live data
    const updatePrice = () => {
      const newPrice = (Math.random() * 100 + 18000).toFixed(2);
      candlestickSeries.update({ time: Date.now(), open: newPrice, high: newPrice * 1.02, low: newPrice * 0.98, close: newPrice });
    };

    const interval = setInterval(updatePrice, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ textAlign: "center", marginTop: "3rem", padding: "1rem", backgroundColor: "#2b2b2b", borderRadius: "8px" }}>
      <Typography variant="h6" sx={{ color: "primary.main", fontWeight: "bold", marginBottom: "1rem" }}>
        📈 Live Trading Chart
      </Typography>
      <div ref={chartContainerRef} style={{ width: "100%", height: "300px" }}></div>
    </Box>
  );
};

export default TradingChart;
