import { createContext, useContext, useMemo, useState } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";

const ThemeModeContext = createContext();

export const CustomThemeProvider = ({ children }) => {
  const [mode, setMode] = useState("dark");

  const toggleTheme = () => {
    setMode((prev) => (prev === "light" ? "dark" : "light"));
  };

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === "dark"
            ? {
                background: { default: "#0d1117", paper: "#161b22" },
                text: { primary: "#fff", secondary: "#aaa" },
              }
            : {
                background: { default: "#f5f5f5", paper: "#fff" },
                text: { primary: "#000", secondary: "#555" },
              }),
        },
      }),
    [mode]
  );

  return (
    <ThemeModeContext.Provider value={{ mode, toggleTheme }}>
      <ThemeProvider theme={theme}>{children}</ThemeProvider>
    </ThemeModeContext.Provider>
  );
};

export const useThemeMode = () => useContext(ThemeModeContext);
