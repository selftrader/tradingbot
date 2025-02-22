import { Button, Box } from "@mui/material";

const TradeControls = () => {
  return (
    <Box sx={{ display: "flex", gap: 2, mt: 3 }}>
      <Button variant="outlined" sx={{ borderColor: "#FF00D6", color: "#FF00D6", "&:hover": { borderColor: "#7C3AED" } }}>
        Start Trade
      </Button>
      <Button variant="outlined" sx={{ borderColor: "#7C3AED", color: "#7C3AED", "&:hover": { borderColor: "#FF00D6" } }}>
        Stop Trade
      </Button>
    </Box>
  );
};

export default TradeControls;
