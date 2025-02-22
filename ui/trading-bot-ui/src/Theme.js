import { createTheme } from "@mui/material/styles";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#FF00D6" },
    secondary: { main: "#7C3AED" },
    background: { default: "#000000", paper: "#000000" },
    text: { primary: "#ffffff", secondary: "#cccccc" },
  },
  typography: {
    fontFamily: "Roboto, sans-serif",
    h1: {
      fontWeight: "bold",
      background: "linear-gradient(90deg, #FF00D6, #7C3AED)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
    },
  },
});

export  {darkTheme};  // ✅ Fixed missing export
