import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#1e88e5" }, // ✅ Brighter blue
    secondary: { main: "#cfcfcf" }, // ✅ Better visibility
    success: { main: "#4caf50" }, // ✅ Green for success
    warning: { main: "#ffc107" }, // ✅ Yellow for alerts
    error: { main: "#ff3d00" }, // ✅ Red for errors
    background: { default: "#121820", paper: "#1a2027" }, // ✅ Slightly lighter for better readability
    text: { primary: "#e0e0e0", secondary: "#cfcfcf" }, // ✅ Improved text contrast
  },
  typography: {
    fontFamily: "Roboto, sans-serif",
    fontSize: 15, // ✅ Slightly larger for readability
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: "bold",
          borderRadius: 8,
          backgroundColor: "#1e88e5",
          color: "#ffffff",
          "&:hover": { backgroundColor: "#1565c0", color: "#ffffff" }, // ✅ Better hover effect
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: "#1a2027", // ✅ Lighter for better contrast
          color: "text.primary",
          borderRadius: 10,
          boxShadow: "0px 4px 12px rgba(255, 255, 255, 0.1)", // ✅ Soft glow effect
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#1a2027", // ✅ Matches card color
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: "text.primary", // ✅ Ensuring all typography elements have readable colors
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: "bold",
          color: "#ffffff",
          "&.MuiChip-colorPrimary": { backgroundColor: "#1e88e5" }, // ✅ Improved primary chip color
          "&.MuiChip-colorSecondary": { backgroundColor: "#ffc107", color: "#000" }, // ✅ Warning chip
          "&.MuiChip-colorError": { backgroundColor: "#ff3d00" }, // ✅ Error chip
        },
      },
    },
    MuiTable: {
      styleOverrides: {
        root: {
          backgroundColor: "background.paper", // ✅ Matches other elements
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: "primary.main", // ✅ Bright header background
          "& th": {
            color: "#ffffff", // ✅ White text for better readability
            fontWeight: "bold",
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            color: "text.primary",
            "& fieldset": { borderColor: "primary.main" }, // ✅ Blue border
            "&:hover fieldset": { borderColor: "#1565c0" },
          },
          "& .MuiInputLabel-root": {
            color: "text.secondary",
          },
        },
      },
    },
  },
});

export default theme;
