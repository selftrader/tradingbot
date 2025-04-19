import React from "react";
import { Fab, Tooltip, Zoom } from "@mui/material";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";

const FloatingCTA = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <Zoom in>
      <Tooltip title="Launch your journey" placement="left">
        <Fab
          sx={{
            position: "fixed",
            bottom: 20,
            right: 20,
            background: "linear-gradient(145deg, #00f2fe, #4facfe)",
            color: "#fff",
            boxShadow: "0px 4px 24px rgba(0, 175, 239, 0.5)",
            ":hover": {
              background: "linear-gradient(145deg, #00c6fb, #005bea)",
              transform: "scale(1.05)",
            },
          }}
          onClick={scrollToTop}
        >
          <RocketLaunchIcon />
        </Fab>
      </Tooltip>
    </Zoom>
  );
};

export default FloatingCTA;
