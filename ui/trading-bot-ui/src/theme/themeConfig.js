import { createTheme } from "@mui/material/styles";

const tradingTheme = createTheme({
  palette: {
    primary: { main: "#007bff" }, // Trading Blue
    secondary: { main: "#28a745" }, // Profit Green
    error: { main: "#dc3545" }, // Loss Red
    background: { default: "#f4f6f9", paper: "#ffffff" },
    text: { primary: "#212529", secondary: "#6c757d" },
  },
  typography: {
    fontFamily: "'Inter', sans-serif",
    button: { textTransform: "none", fontWeight: "bold" },
  },
});

export default tradingTheme;
