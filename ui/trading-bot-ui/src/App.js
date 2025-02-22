import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ThemeProvider, CssBaseline } from "@mui/material";
import {darkTheme} from "./Theme";

import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import LiveUpdates from "./pages/LiveUpdates";  // ✅ Fixed wrong import
import ConfigPage from "./pages/ConfigPage";  
import StockAnalysisPage from "./pages/StockAnalysisPage";  
import Footer from "./components/Footer";

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/liveupdate" element={<LiveUpdates />} />
          <Route path="/config" element={<ConfigPage />} />
          <Route path="/analyze" element={<StockAnalysisPage />} />
        </Routes>
        <Footer />
      </Router>
    </ThemeProvider>
  );
}

export default App;
