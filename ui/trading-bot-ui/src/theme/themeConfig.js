import { createTheme } from "@mui/material/styles";

const lightTheme = {
  palette: {
    mode: "light",
    primary: { main: "#1E3A8A" }, // Deep Royal Blue
    secondary: { main: "#22D3EE" }, // Cyan for highlights
    success: { main: "#16A34A" }, // Green for profits
    error: { main: "#DC2626" }, // Red for losses
    background: { default: "#F3F4F6", paper: "#ffffff" },
    text: { primary: "#111827", secondary: "#6B7280" },
  },
  typography: {
    fontFamily: "'Inter', sans-serif",
    h1: { fontSize: "2.2rem", fontWeight: "bold" },
    h2: { fontSize: "1.8rem", fontWeight: "bold" },
    button: { textTransform: "none", fontWeight: "bold" },
  },
};

const darkTheme = {
  palette: {
    mode: "dark",
    primary: { main: "#1E3A8A" },
    secondary: { main: "#22D3EE" },
    success: { main: "#16A34A" },
    error: { main: "#EF4444" },
    background: { default: "#111827", paper: "#1F2937" },
    text: { primary: "#E5E7EB", secondary: "#9CA3AF" },
  },
};

export { lightTheme, darkTheme };