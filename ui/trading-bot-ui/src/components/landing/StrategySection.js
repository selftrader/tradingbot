// src/components/landing/StrategySection.jsx
import { Box, Typography, Container, Grid } from "@mui/material";
import { motion } from "framer-motion";

const StrategySection = () => {
  return (
    <Box sx={{ py: 10, bgcolor: "#111" }}>
      <Container maxWidth="lg">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Typography
            variant="h4"
            sx={{ color: "#00E5FF", fontWeight: 600, mb: 3 }}
          >
            Proven AI Strategy
          </Typography>
          <Typography variant="body1" sx={{ color: "#ccc", maxWidth: 700 }}>
            Our trading AI is trained with years of historical data, adaptive
            logic, and smart risk management. It scans opportunities, executes
            trades, and evolves — so you stay ahead of the market.
          </Typography>
        </motion.div>

        <Grid container spacing={4} mt={4}>
          {[
            {
              title: "Backtested Over 5 Years",
              desc: "Using real historical market data",
            },
            {
              title: "85% Win Ratio",
              desc: "Optimized with smart entry/exit signals",
            },
            {
              title: "Real-Time AI Execution",
              desc: "No emotions, just logic & automation",
            },
          ].map((item, i) => (
            <Grid item xs={12} md={4} key={i}>
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.2 }}
              >
                <Box
                  sx={{
                    p: 4,
                    borderRadius: 2,
                    bgcolor: "#1a1a1a",
                    color: "#fff",
                    border: "1px solid #222",
                  }}
                >
                  <Typography variant="h6" sx={{ mb: 1, color: "#00E5FF" }}>
                    {item.title}
                  </Typography>
                  <Typography variant="body2" sx={{ color: "#ccc" }}>
                    {item.desc}
                  </Typography>
                </Box>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default StrategySection;
