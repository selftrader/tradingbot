import React, { createContext, useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { lightTheme, darkTheme } from "../theme/themeConfig";

export const ThemeContext = createContext();

const ThemeProviderWrapper = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev);
  };

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
      <ThemeProvider theme={createTheme(isDarkMode ? darkTheme : lightTheme)}>
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProviderWrapper;
