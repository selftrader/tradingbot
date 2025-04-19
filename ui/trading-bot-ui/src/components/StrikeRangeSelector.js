import { Select, MenuItem, InputLabel, FormControl } from "@mui/material";

export default function StrikeRangeSelector({ value, onChange }) {
  return (
    <FormControl fullWidth>
      <InputLabel>Strike Range (ATM ±)</InputLabel>
      <Select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        label="Strike Range"
      >
        <MenuItem value={10}>±10</MenuItem>
        <MenuItem value={20}>±20</MenuItem>
        <MenuItem value={30}>±30</MenuItem>
      </Select>
    </FormControl>
  );
}
