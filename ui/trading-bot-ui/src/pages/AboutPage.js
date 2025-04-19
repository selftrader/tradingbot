import { Box, Container, Typography, Divider } from "@mui/material";
import { motion } from "framer-motion";

const AboutPage = () => {
  return (
    <Box sx={{ py: 10, px: 2, bgcolor: "#0A0B0E", color: "#fff" }}>
      <Container maxWidth="md">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Typography variant="h3" fontWeight="bold" mb={3} color="#00E5FF">
            About Growth Quantix
          </Typography>

          <Typography variant="body1" color="grey.300" mb={2}>
            Growth Quantix is building a revolutionary AI-powered trading
            platform designed to democratize access to institutional-grade tools
            for retail traders.
          </Typography>

          <Typography variant="body1" color="grey.300" mb={2}>
            With powerful backtesting, intelligent signal generation, real-time
            execution, and deep analytics, we empower traders to act smarter,
            faster, and more profitably.
          </Typography>

          <Divider sx={{ my: 4, bgcolor: "#00E5FF" }} />

          <Typography variant="h5" fontWeight="bold" mb={1}>
            Mission
          </Typography>
          <Typography variant="body2" color="grey.400" mb={3}>
            To build India's smartest, fastest, and most reliable AI trading
            system that puts automation in the hands of every trader.
          </Typography>

          <Typography variant="h5" fontWeight="bold" mb={1}>
            Values
          </Typography>
          <Typography variant="body2" color="grey.400">
            💡 Innovation | 🔐 Security | 📈 Performance | 🙌 Community
          </Typography>
        </motion.div>
      </Container>
    </Box>
  );
};

export default AboutPage;
