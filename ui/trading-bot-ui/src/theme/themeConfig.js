import { createTheme } from "@mui/material/styles";

export const lightTheme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#6a11cb" }, // Light mode primary accent
    background: { default: "#f9f9f9", paper: "#ffffff" },
    text: { primary: "#222222", secondary: "#555" },
  },
  typography: {
    fontFamily: "'Poppins', sans-serif",
    fontWeightBold: 700,
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#ffffff",
          boxShadow: "none",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: "bold",
          borderRadius: "30px",
          padding: "10px 20px",
        },
      },
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#ff44ff" },  // Neon purple-pink accent
    background: { default: "#000000", paper: "#121212" },  // True black theme
    text: { primary: "#ffffff", secondary: "#bbbbbb" },
  },
  typography: {
    fontFamily: "'Poppins', sans-serif",
    fontWeightBold: 700,
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#000000", 
          boxShadow: "none",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: "bold",
          borderRadius: "30px",
          padding: "10px 20px",
          border: "1px solid #ff44ff",  // Neon pink border
          color: "#ffffff",
          "&:hover": {
            backgroundColor: "rgba(255, 68, 255, 0.2)",
          },
        },
      },
    },
  },
});