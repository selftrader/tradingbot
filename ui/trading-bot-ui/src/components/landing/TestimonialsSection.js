import React from "react";
import { Box, Container, Typography, Grid, Paper, Avatar } from "@mui/material";

const testimonials = [
  {
    name: "Ravi M.",
    comment: "Quantix's breakout AI replaced hours of manual charting!",
  },
  {
    name: "Neha S.",
    comment: "My options win rate jumped by 30% using the scalping bot.",
  },
  {
    name: "Arjun D.",
    comment: "The sector rotation AI outperformed my ETF strategy easily.",
  },
];

const TestimonialsSection = () => {
  return (
    <Box sx={{ bgcolor: "#0b1320", color: "#ffffff", py: 10 }}>
      <Container>
        <Typography
          variant="h4"
          fontWeight="bold"
          align="center"
          sx={{ mb: 6 }}
        >
          What Our Traders Say
        </Typography>
        <Grid container spacing={4}>
          {testimonials.map((t, i) => (
            <Grid item xs={12} md={4} key={i}>
              <Paper
                sx={{
                  p: 4,
                  background: "#061120",
                  border: "1px solid #00aeef",
                }}
              >
                <Avatar
                  sx={{ bgcolor: "#00aeef", width: 56, height: 56, mb: 2 }}
                >
                  {t.name[0]}
                </Avatar>
                <Typography sx={{ fontStyle: "italic", opacity: 0.85 }}>
                  "{t.comment}"
                </Typography>
                <Typography
                  variant="subtitle2"
                  sx={{ mt: 2, fontWeight: "bold" }}
                >
                  – {t.name}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default TestimonialsSection;
