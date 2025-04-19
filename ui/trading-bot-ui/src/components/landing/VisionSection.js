import { Box, Typography, Button, Grid, useTheme } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import visionImg from "../../assets/icons/vision_ai.svg"; // 🧠 Make sure this file exists

const VisionSection = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  return (
    <Box
      id="vision"
      sx={{
        py: 12,
        px: 3,
        background:
          theme.palette.mode === "dark"
            ? "linear-gradient(135deg, #0A0B0E 0%, #1a1d1f 100%)"
            : "linear-gradient(135deg, #F4F6F8 0%, #EAECEE 100%)",
        backgroundImage: `url('/assets/pattern.svg')`,
        backgroundRepeat: "repeat",
        backgroundSize: "300px",
        color: theme.palette.text.primary,
        overflow: "hidden",
      }}
    >
      <Grid
        container
        spacing={6}
        alignItems="center"
        justifyContent="center"
        maxWidth="lg"
        sx={{ mx: "auto" }}
      >
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
          >
            <Typography variant="h4" fontWeight="bold" mb={3}>
              Our Vision
            </Typography>

            <Typography variant="body1" mb={2} color="text.secondary">
              At <strong>Growth Quantix</strong>, our vision is to empower
              retail traders worldwide by providing them with cutting-edge,
              AI-driven trading solutions that level the playing field in
              financial markets.
            </Typography>

            <Typography variant="body1" mb={2} color="text.secondary">
              We aim to create a future where every trader—regardless of
              experience— can harness the full potential of automation, advanced
              analytics, and intelligent risk management to make smarter,
              data-backed decisions.
            </Typography>

            <Typography variant="body1" mb={2} color="text.secondary">
              By offering retail traders the same advanced tools and insights
              once reserved for institutions, we’re not just shaping
              trading—we’re building a future of financial independence.
            </Typography>

            <Typography variant="body1" color="text.secondary">
              <strong>Growth Quantix</strong> is committed to continual
              innovation—pushing boundaries in AI trading and empowering traders
              with real, profitable impact.
            </Typography>

            <Button
              variant="outlined"
              size="large"
              sx={{
                mt: 4,
                borderColor: "#00E5FF",
                color: "#00E5FF",
                fontWeight: "bold",
                "&:hover": {
                  bgcolor: "#00E5FF",
                  color: "#000",
                },
              }}
              onClick={() => navigate("/about")}
            >
              Learn More
            </Button>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
          >
            <Box
              component="img"
              src={visionImg}
              alt="AI Vision"
              sx={{
                width: "100%",
                maxWidth: 520,
                mx: "auto",
                display: "block",
              }}
            />
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VisionSection;
