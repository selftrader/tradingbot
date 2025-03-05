import React, { useEffect } from "react";
import { Box, Container } from "@mui/material";
import { Outlet, useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import { isAuthenticated } from "../../services/authService";

const Layout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate("/login"); // ✅ Redirect to login if not authenticated
    }
  }, [navigate]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Navbar />  {/* ✅ Navbar now contains navigation buttons */}
      <Container sx={{ mt: 10 }}>
        <Outlet />  {/* ✅ This ensures pages load when clicking navigation buttons */}
      </Container>
    </Box>
  );
};

export default Layout;
