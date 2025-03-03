import { createTheme } from "@mui/material/styles";

const lightTheme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#1E3A8A" }, // Deep Royal Blue
    secondary: { main: "#22D3EE" },
    text: { primary: "#111827", secondary: "#6B7280" }, // ✅ Improved Contrast
    background: { default: "#F3F4F6", paper: "#ffffff" },
  },
});

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#1E3A8A" },
    secondary: { main: "#22D3EE" },
    text: { primary: "#E5E7EB", secondary: "#9CA3AF" }, // ✅ Improved Contrast
    background: { default: "#111827", paper: "#1F2937" },
  },
});

export { lightTheme, darkTheme };
