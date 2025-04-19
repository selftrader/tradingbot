import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  Box,
} from "@mui/material";

const OptionChainTable = ({ chain = [], atm, instrumentType }) => {
  const getCellStyle = (type, strike) => {
    if (!atm) return {};
    if (type === "CE" && strike < atm) return { backgroundColor: "#fff3e0" };
    if (type === "PE" && strike > atm) return { backgroundColor: "#fff3e0" };
    return {};
  };

  if (!Array.isArray(chain) || chain.length === 0) {
    return (
      <Typography variant="body2" sx={{ mt: 2, color: "gray" }}>
        No option chain data available.
      </Typography>
    );
  }

  return (
    <Box mt={2}>
      <Typography variant="h6" gutterBottom>
        Option Chain View
      </Typography>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell rowSpan={2}>Strike</TableCell>
            <TableCell colSpan={3} align="center">
              Call (CE)
            </TableCell>
            <TableCell colSpan={3} align="center">
              Put (PE)
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell>LTP</TableCell>
            <TableCell>IV</TableCell>
            <TableCell>OI</TableCell>
            <TableCell>LTP</TableCell>
            <TableCell>IV</TableCell>
            <TableCell>OI</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {chain.map((row, idx) => (
            <TableRow
              key={idx}
              sx={{
                backgroundColor:
                  row.strike_price === atm ? "#e3f2fd" : "inherit",
              }}
            >
              <TableCell>
                <strong>{row.strike_price}</strong>
              </TableCell>
              <TableCell sx={getCellStyle("CE", row.strike_price)}>
                {row.ce?.ltp?.toFixed(2) ?? "-"}
              </TableCell>
              <TableCell>{row.ce?.iv?.toFixed(2) ?? "-"}</TableCell>
              <TableCell>{row.ce?.oi ?? "-"}</TableCell>
              <TableCell sx={getCellStyle("PE", row.strike_price)}>
                {row.pe?.ltp?.toFixed(2) ?? "-"}
              </TableCell>
              <TableCell>{row.pe?.iv?.toFixed(2) ?? "-"}</TableCell>
              <TableCell>{row.pe?.oi ?? "-"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
};

export default OptionChainTable;
