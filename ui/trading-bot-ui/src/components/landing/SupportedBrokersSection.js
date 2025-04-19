// src/components/landing/SupportedBrokersSection.jsx
import {
  Box,
  Typography,
  useTheme,
  useMediaQuery,
  Tooltip,
} from "@mui/material";
import dhan from "../../assets/brokers/dhan_logo.png";
import zerodha from "../../assets/brokers/zerodha_logo.png";
import upstox from "../../assets/brokers/upstox_logo.png";
import angel from "../../assets/brokers/AO_logo.png";
import fyers from "../../assets/brokers/fyers_logo.png";

const brokers = [
  { name: "Dhan", logo: dhan },
  { name: "Zerodha", logo: zerodha },
  { name: "Upstox", logo: upstox },
  { name: "Angel One", logo: angel },
  { name: "Fyers", logo: fyers },
];

const SupportedBrokersSection = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <Box
      sx={{
        bgcolor: "#050D1B",
        py: 12,
        textAlign: "center",
        position: "relative",
        overflow: "hidden",
        background: `
          radial-gradient(circle at center, rgba(0, 229, 255, 0.06), transparent 70%),
          linear-gradient(180deg, #0A0B0E 0%, #050D1B 100%)
        `,
      }}
    >
      {/* Section Content */}
      <Box sx={{ position: "relative", zIndex: 2 }}>
        <Typography variant="h4" fontWeight="bold" color="#00E5FF" mb={2}>
          Supported Brokers
        </Typography>
        <Typography variant="body1" color="grey.400" mb={6}>
          Seamlessly connect your account with top Indian brokers
        </Typography>

        {/* ✨ Circular Orbit Layout (Desktop) */}
        {!isMobile && (
          <Box
            sx={{
              position: "relative",
              width: 360,
              height: 360,
              mx: "auto",
              animation: "spin 50s linear infinite",
            }}
          >
            {brokers.map((broker, idx) => {
              const angle = (360 / brokers.length) * idx;
              const radius = 120; // ✅ Reduced from 180 → tighter layout
              const x = radius * Math.cos((angle * Math.PI) / 180);
              const y = radius * Math.sin((angle * Math.PI) / 180);

              return (
                <Tooltip key={idx} title={broker.name} arrow>
                  <Box
                    sx={{
                      position: "absolute",
                      left: "50%",
                      top: "50%",
                      transform: `translate(-50%, -50%) translate(${x}px, ${y}px)`,
                      borderRadius: "50%",
                      width: 80,
                      height: 80,
                      backdropFilter: "blur(6px)",
                      background: "rgba(255,255,255,0.08)",
                      border: "1px solid rgba(255,255,255,0.1)",
                      boxShadow: "0 8px 16px rgba(0, 229, 255, 0.15)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      transition: "transform 0.3s ease",
                      "&:hover": {
                        transform: `translate(-50%, -50%) translate(${x}px, ${y}px) scale(1.1)`,
                        boxShadow: "0 12px 24px rgba(0, 229, 255, 0.3)",
                      },
                    }}
                  >
                    <Box
                      component="img"
                      src={broker.logo}
                      alt={broker.name}
                      sx={{
                        maxWidth: 45,
                        maxHeight: 45,
                        filter: "brightness(1.8) contrast(1.2)", // ✅ Lighten logo appearance
                      }}
                    />
                  </Box>
                </Tooltip>
              );
            })}
          </Box>
        )}

        {/* 📱 Mobile Scrollable Layout */}
        {isMobile && (
          <Box
            sx={{
              display: "flex",
              overflowX: "auto",
              gap: 4,
              justifyContent: "center",
              px: 2,
              pt: 4,
              pb: 2,
              scrollbarWidth: "none",
              "&::-webkit-scrollbar": { display: "none" },
            }}
          >
            {brokers.map((broker, idx) => (
              <Box
                key={idx}
                sx={{
                  flex: "0 0 auto",
                  width: 80,
                  height: 80,
                  bgcolor: "#1A1A1D",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: "0 0 18px rgba(0,255,255,0.2)",
                }}
              >
                <Box
                  component="img"
                  src={broker.logo}
                  alt={broker.name}
                  sx={{
                    maxWidth: 40,
                    maxHeight: 40,
                    filter: "brightness(1.6) contrast(1.1)",
                  }}
                />
              </Box>
            ))}
          </Box>
        )}
      </Box>

      {/* 🔁 Animation Keyframe */}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
    </Box>
  );
};

export default SupportedBrokersSection;
