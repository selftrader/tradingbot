import { useTheme } from "@mui/material/styles";
import { Switch } from "@mui/material";
import { useEffect, useState } from "react";

const ThemeToggle = () => {
  const [mode, setMode] = useState(localStorage.getItem("theme") || "light");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", mode);
    localStorage.setItem("theme", mode);
  }, [mode]);

  return (
    <Switch
      checked={mode === "dark"}
      onChange={() => setMode(mode === "dark" ? "light" : "dark")}
    />
  );
};

export default ThemeToggle;
