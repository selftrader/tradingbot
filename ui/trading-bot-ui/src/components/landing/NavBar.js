import React, { useState, lazy, Suspense } from "react";
import { Box, Typography, Button, Menu, MenuItem, Fade } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { isAuthenticated } from "../../services/authService"; // make sure this exists

const LazyAuthModal = lazy(() => import("../auth/AuthModal"));

const NavBar = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [activeMenu, setActiveMenu] = useState(null);
  const [authOpen, setAuthOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);

  const isUserAuthenticated = isAuthenticated();

  const handleOpen = (event, menuName) => {
    setAnchorEl(event.currentTarget);
    setActiveMenu(menuName);
  };

  const handleClose = () => {
    setAnchorEl(null);
    setActiveMenu(null);
  };

  const menuData = {
    Products: [
      { label: "AI Agent", href: "#ai-agent" },
      { label: "Backtester", href: "#backtest" },
      { label: "Strategy Designer", href: "#strategy" },
    ],
    Solutions: [
      { label: "Retail Traders", href: "#retail" },
      { label: "Institutions", href: "#institutions" },
    ],
    Resources: [
      { label: "Pricing", href: "#pricing" },
      { label: "Docs", href: "#docs" },
      { label: "Blog", href: "#blog" },
    ],
  };

  const handleScrollTo = (id) => {
    handleClose();
    const el = document.querySelector(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          px: 4,
          py: 2,
          alignItems: "center",
          bgcolor: "#0A0B0E",
          position: "sticky",
          top: 0,
          zIndex: 1000,
          boxShadow: "0 1px 6px rgba(0,0,0,0.3)",
        }}
      >
        <Typography
          variant="h5"
          sx={{ fontWeight: 700, color: "#00E5FF", cursor: "pointer" }}
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        >
          GrowthQuantix
        </Typography>

        <Box sx={{ display: "flex", gap: 4, alignItems: "center" }}>
          {Object.keys(menuData).map((menu) => (
            <Box
              key={menu}
              onMouseEnter={(e) => handleOpen(e, menu)}
              onMouseLeave={handleClose}
              sx={{
                position: "relative",
                color: "#fff",
                fontWeight: 500,
                cursor: "pointer",
                "&:hover": { color: "#00E5FF" },
              }}
            >
              <Typography>{menu}</Typography>
              <Menu
                anchorEl={anchorEl}
                open={activeMenu === menu}
                onClose={handleClose}
                TransitionComponent={Fade}
                anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
                transformOrigin={{ vertical: "top", horizontal: "left" }}
                PaperProps={{
                  sx: {
                    bgcolor: "#1A1A1D",
                    color: "#fff",
                    borderRadius: 1,
                    boxShadow: 5,
                    minWidth: 180,
                  },
                }}
              >
                {menuData[menu].map((item, idx) => (
                  <MenuItem
                    key={idx}
                    onClick={() => handleScrollTo(item.href)}
                    sx={{
                      "&:hover": {
                        bgcolor: "#00E5FF",
                        color: "#000",
                      },
                    }}
                  >
                    {item.label}
                  </MenuItem>
                ))}
              </Menu>
            </Box>
          ))}

          {isUserAuthenticated ? (
            <Button
              variant="contained"
              onClick={() => navigate("/dashboard")}
              sx={{
                bgcolor: "#00E5FF",
                color: "#000",
                fontWeight: "bold",
                borderRadius: "999px",
                px: 3,
                "&:hover": {
                  bgcolor: "#00B2CC",
                },
              }}
            >
              Go to Dashboard
            </Button>
          ) : (
            <>
              <Button
                variant="outlined"
                color="inherit"
                sx={{ borderColor: "#00E5FF", color: "#00E5FF" }}
                onClick={() => {
                  setIsLogin(true);
                  setAuthOpen(true);
                }}
              >
                Sign In
              </Button>
              <Button
                variant="contained"
                sx={{
                  bgcolor: "#00E5FF",
                  color: "#000",
                  fontWeight: "bold",
                  borderRadius: "999px",
                  px: 3,
                  "&:hover": {
                    bgcolor: "#00B2CC",
                  },
                }}
                onClick={() => {
                  setIsLogin(false);
                  setAuthOpen(true);
                }}
              >
                Sign Up
              </Button>
            </>
          )}
        </Box>
      </Box>

      <Suspense fallback={<Box>Loading...</Box>}>
        {authOpen && (
          <LazyAuthModal
            open={authOpen}
            handleClose={() => setAuthOpen(false)}
            onLoginSuccess={() => {
              setAuthOpen(false);
              navigate("/dashboard");
            }}
            isLogin={isLogin}
            setIsLogin={setIsLogin}
          />
        )}
      </Suspense>
    </>
  );
};

export default NavBar;
