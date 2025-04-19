import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  Container,
  useScrollTrigger,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";

const sections = [
  { label: "Home", id: "hero" },
  { label: "About", id: "about" },
  { label: "Features", id: "features" },
  { label: "Backtesting", id: "backtesting" },
  { label: "Vision", id: "vision" },
  { label: "Why Us", id: "why" },
];

const ScrollNavHeader = () => {
  const navigate = useNavigate();
  const trigger = useScrollTrigger({ threshold: 50 });

  const handleScroll = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <AppBar
      position="fixed"
      elevation={trigger ? 4 : 0}
      color="default"
      sx={{
        transition: "all 0.3s ease-in-out",
        backgroundColor: trigger ? "background.paper" : "transparent",
        backdropFilter: "blur(10px)",
        zIndex: 1200,
      }}
    >
      <Container maxWidth="lg">
        <Toolbar
          disableGutters
          sx={{ display: "flex", justifyContent: "space-between" }}
        >
          {/* Logo / Brand */}
          <Box
            sx={{ display: "flex", alignItems: "center", cursor: "pointer" }}
            onClick={() => handleScroll("hero")}
          >
            <Box
              component="img"
              src="/logo192.png"
              alt="GrowthQuantix Logo"
              sx={{ width: 36, height: 36, mr: 1 }}
            />
            <Typography variant="h6" fontWeight="bold">
              Growth Quantix
            </Typography>
          </Box>

          {/* Navigation */}
          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            {sections.map((item) => (
              <Button
                key={item.id}
                color="inherit"
                onClick={() => handleScroll(item.id)}
                sx={{ fontWeight: 500, fontSize: "0.95rem" }}
              >
                {item.label}
              </Button>
            ))}
            <ThemeToggle />
            <Button
              variant="contained"
              sx={{ ml: 2 }}
              onClick={() => navigate("/dashboard")}
            >
              Launch App
            </Button>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default ScrollNavHeader;
