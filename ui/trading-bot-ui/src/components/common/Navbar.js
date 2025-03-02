import React, { useState } from "react";
import { AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, ListItemText } from "@mui/material";
import { Menu as MenuIcon, Close } from "@mui/icons-material";
import ThemeToggle from "../settings/ThemeToggle";

const Navbar = ({ toggleTheme, isDarkMode }) => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <AppBar position="fixed" color="primary">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu" onClick={() => setOpen(true)}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1, textAlign: { xs: "center", md: "left" } }}>
            Algo Trading Bot
          </Typography>
          <ThemeToggle toggleTheme={toggleTheme} isDarkMode={isDarkMode} />
        </Toolbar>
      </AppBar>

      {/* Responsive Drawer Menu */}
      <Drawer anchor="left" open={open} onClose={() => setOpen(false)}>
        <IconButton sx={{ alignSelf: "flex-end", m: 1 }} onClick={() => setOpen(false)}>
          <Close />
        </IconButton>
        <List>
          {["Dashboard", "Trading", "Settings"].map((text) => (
            <ListItem button key={text}>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List>
      </Drawer>
    </>
  );
};

export default Navbar;
