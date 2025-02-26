import { createTheme } from "@mui/material/styles";

export const lightTheme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#6a11cb" },
    background: { default: "#ffffff", paper: "#f9f9f9" },
    text: { primary: "#1a1a1a", secondary: "#444" },
  },
  typography: {
    fontFamily: "'Poppins', sans-serif",
    fontWeightBold: 700,
  },
  components: {
    MuiIconButton: {
      styleOverrides: {
        root: {
          color: "#222",
          "&:hover": {
            color: "#000",
          },
        },
      },
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#ff44ff" },
    background: { default: "#121212", paper: "#1e1e1e" },
    text: { primary: "#ffffff", secondary: "#bbb" },
  },
  typography: {
    fontFamily: "'Poppins', sans-serif",
    fontWeightBold: 700,
  },
  components: {
    MuiIconButton: {
      styleOverrides: {
        root: {
          color: "#fff",
          "&:hover": {
            color: "#ddd",
          },
        },
      },
    },
  },
});
