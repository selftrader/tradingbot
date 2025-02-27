import React, { createContext } from "react";
import { ThemeProvider } from "@mui/material/styles";
import tradingTheme from "../theme/themeConfig";

export const ThemeContext = createContext();

const ThemeProviderWrapper = ({ children }) => {
  return (
    <ThemeContext.Provider value={{}}>
      <ThemeProvider theme={tradingTheme}>{children}</ThemeProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProviderWrapper;
