import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { time: "09:00", price: 120 },
  { time: "10:00", price: 135 },
  { time: "11:00", price: 145 },
  { time: "12:00", price: 155 },
];

const LiveChart = () => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="time" stroke="#ffffff" />
        <YAxis stroke="#ffffff" />
        <Tooltip />
        <Line type="monotone" dataKey="price" stroke="#FF00D6" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default LiveChart;
