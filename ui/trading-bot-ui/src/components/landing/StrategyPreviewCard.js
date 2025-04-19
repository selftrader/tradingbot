import { Box, Typography, Paper, Grid } from "@mui/material";
import { motion } from "framer-motion";

const stats = [
  { label: "Net Profit", value: "$6,244" },
  { label: "Trades", value: "128" },
  { label: "Win Rate", value: "79.25%" },
  { label: "Max Drawdown", value: "-12.1%" },
];

const StrategyPreviewCard = () => {
  return (
    <Box sx={{ py: 6, backgroundColor: "background.paper" }}>
      <Grid container spacing={3} justifyContent="center">
        {stats.map((item, index) => (
          <Grid item xs={12} sm={6} md={3} key={item.label}>
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <Paper
                elevation={3}
                sx={{
                  p: 3,
                  textAlign: "center",
                  borderRadius: 4,
                  bgcolor: "background.default",
                  color: "text.primary",
                }}
              >
                <Typography variant="h4" fontWeight={600}>
                  {item.value}
                </Typography>
                <Typography variant="subtitle1" sx={{ opacity: 0.75 }}>
                  {item.label}
                </Typography>
              </Paper>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default StrategyPreviewCard;
