import { Table, TableHead, TableBody, TableRow, TableCell, Paper } from "@mui/material";

const BacktestTradeLog = ({ trades }) => (
  <Paper sx={{ mt: 3 }}>
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>Entry</TableCell>
          <TableCell>Exit</TableCell>
          <TableCell>Direction</TableCell>
          <TableCell>Entry Price</TableCell>
          <TableCell>Exit Price</TableCell>
          <TableCell>P&L</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {trades.map((t, i) => (
          <TableRow key={i}>
            <TableCell>{t.entry_date}</TableCell>
            <TableCell>{t.exit_date}</TableCell>
            <TableCell>{t.direction}</TableCell>
            <TableCell>{t.entry_price}</TableCell>
            <TableCell>{t.exit_price}</TableCell>
            <TableCell>{t.pnl}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </Paper>
);

export default BacktestTradeLog;
