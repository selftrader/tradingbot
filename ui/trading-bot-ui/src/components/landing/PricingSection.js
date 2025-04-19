import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  useTheme,
  Chip,
  Divider,
} from "@mui/material";

const plans = [
  {
    title: "Basic",
    price: "₹4999/mo",
    subtitle: "Best for Beginners",
    features: ["Live Signals", "1 Strategy", "Email Alerts", "Basic Dashboard"],
    color: "#1c2b39",
    highlight: false,
  },
  {
    title: "Pro",
    price: "₹9999/mo",
    subtitle: "Most Popular",
    features: [
      "Multi-Strategy AI",
      "Priority Support",
      "Telegram Alerts",
      "Advanced Dashboard",
    ],
    color: "linear-gradient(135deg, #00e5ff, #005eff)",
    highlight: true,
  },
  {
    title: "Elite",
    price: "₹14999/mo",
    subtitle: "For Active Traders",
    features: [
      "Full AI Automation",
      "Smart Exit & Entry",
      "Broker Integration",
      "Real-time Optimization",
    ],
    color: "#131b25",
    highlight: false,
  },
];

const PlansSection = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === "dark";

  return (
    <Box
      id="pricing"
      py={10}
      px={3}
      sx={{
        bgcolor: isDark ? "#0a1929" : "#f4f6f8",
        color: isDark ? "#fff" : "#000",
      }}
    >
      <Typography
        variant="h4"
        align="center"
        fontWeight="bold"
        mb={1}
        sx={{ color: theme.palette.primary.main }}
      >
        Pricing Plans
      </Typography>
      <Typography align="center" sx={{ mb: 6, opacity: 0.8 }}>
        Pick the plan that suits your trading journey.
      </Typography>

      <Grid container spacing={4} justifyContent="center">
        {plans.map((plan, index) => {
          const isPro = plan.highlight;

          return (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  bgcolor: isPro ? undefined : plan.color,
                  background: isPro ? plan.color : undefined,
                  color: isPro ? "#000" : "#fff",
                  boxShadow: isPro ? 12 : 4,
                  transform: isPro ? "scale(1.05)" : "none",
                  transition: "all 0.3s ease-in-out",
                  borderRadius: 3,
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  {isPro && (
                    <Chip
                      label="Most Popular"
                      color="secondary"
                      size="small"
                      sx={{
                        position: "absolute",
                        top: 16,
                        right: 16,
                        fontWeight: "bold",
                      }}
                    />
                  )}

                  <Typography variant="h5" fontWeight="bold" gutterBottom>
                    {plan.title}
                  </Typography>
                  <Typography variant="subtitle2" sx={{ mb: 2 }}>
                    {plan.subtitle}
                  </Typography>

                  <Typography variant="h3" fontWeight="bold">
                    {plan.price}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.8 }}>
                    Plus includeing GST
                  </Typography>

                  <Divider
                    sx={{
                      my: 2,
                      borderColor: isPro ? "#000" : "rgba(255,255,255,0.2)",
                    }}
                  />

                  <Box component="ul" sx={{ pl: 2, mb: 4 }}>
                    {plan.features.map((feat, idx) => (
                      <li key={idx} style={{ marginBottom: 8 }}>
                        <Typography variant="body1">{feat}</Typography>
                      </li>
                    ))}
                  </Box>

                  <Button
                    variant="contained"
                    fullWidth
                    sx={{
                      borderRadius: "30px",
                      fontWeight: 600,
                      bgcolor: isPro ? "#fff" : "#00E5FF",
                      color: isPro ? "#000" : "#000",
                      "&:hover": {
                        bgcolor: isPro ? "#e0e0e0" : "#00bcd4",
                      },
                    }}
                  >
                    Get Started
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );
};

export default PlansSection;
