import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#ffffff" },
    secondary: { main: "#b0b0b0" },
    accent: { main: "#2196F3" }, // ✅ NEW Accent Color
    background: { default: "#0d1117", paper: "#161b22" }, // ✅ Dark Theme Tweaked
    text: { primary: "#ffffff", secondary: "#b0b0b0" },
  },
  typography: {
    fontFamily: "Roboto, sans-serif",
    fontSize: 14,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          color: "#ffffff",
          "&:hover": { backgroundColor: "#2196F3", color: "#ffffff" }, // ✅ NEW Hover Effect
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#161b22", // ✅ Updated Navbar Color
        },
      },
    },
  },
});

export default theme;
