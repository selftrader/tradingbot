// src/components/StockLiveChart.js
import { useEffect, useRef } from "react";
import { Box } from "@mui/material";
import Chart from "chart.js/auto";
import "chartjs-adapter-date-fns";

const StockLiveChart = ({ instrumentKey, ltp }) => {
  const chartRef = useRef(null);
  const dataRef = useRef([]);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    if (!instrumentKey || !ltp) return;

    const now = new Date();
    dataRef.current.push({ x: now, y: ltp });

    // Keep only last 30 data points
    if (dataRef.current.length > 30) dataRef.current.shift();

    const ctx = chartRef.current?.getContext("2d");

    // Destroy previous instance to avoid canvas reuse error
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    chartInstanceRef.current = new Chart(ctx, {
      type: "line",
      data: {
        datasets: [
          {
            label: instrumentKey,
            data: [...dataRef.current],
            borderWidth: 2,
            borderColor: "blue",
            backgroundColor: "rgba(0,0,255,0.1)",
            tension: 0.3,
            pointRadius: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        scales: {
          x: {
            type: "time",
            time: {
              unit: "second",
              tooltipFormat: "HH:mm:ss",
            },
            ticks: {
              autoSkip: true,
              maxTicksLimit: 10,
            },
          },
          y: {
            beginAtZero: false,
            ticks: {
              precision: 2,
            },
          },
        },
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    });
  }, [ltp, instrumentKey]);

  return (
    <Box sx={{ mt: 2, height: 250 }}>
      <canvas ref={chartRef} />
    </Box>
  );
};

export default StockLiveChart;
