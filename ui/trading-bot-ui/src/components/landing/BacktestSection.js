import { Box, Typography, Container } from "@mui/material";

const BacktestSection = () => {
  return (
    <Box id="backtest" sx={{ py: 10 }}>
      <Container>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Smart Backtesting Engine
        </Typography>
        <Typography variant="body1">
          Test and optimize strategies on historical data with risk control,
          profit/loss, and drawdown analytics.
        </Typography>
      </Container>
    </Box>
  );
};

export default BacktestSection;
