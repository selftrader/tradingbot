import { Line } from "react-chartjs-2";
import { Card, CardContent, Typography } from "@mui/material";
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from "chart.js";
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

const BacktestChart = ({ data }) => {
  const chartData = {
    labels: data.map(d => d.date),
    datasets: [
      {
        label: "Equity Curve",
        data: data.map(d => d.equity),
        borderColor: "green",
        fill: false,
        tension: 0.1,
      },
    ],
  };

  return (
    <Card sx={{ mt: 4 }}>
      <CardContent>
        <Typography variant="h6">📈 Profit / Equity Curve</Typography>
        <Line data={chartData} />
      </CardContent>
    </Card>
  );
};

export default BacktestChart;
