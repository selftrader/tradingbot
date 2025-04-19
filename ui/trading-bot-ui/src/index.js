import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { ThemeProvider, CssBaseline } from "@mui/material";
import { lightTheme, darkTheme } from "./themes/theme";
const container = document.getElementById("root");
const root = createRoot(container);
const currentTheme = localStorage.getItem("theme") || "light";

root.render(
  <React.StrictMode>
    <ThemeProvider theme={currentTheme === "dark" ? darkTheme : lightTheme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
