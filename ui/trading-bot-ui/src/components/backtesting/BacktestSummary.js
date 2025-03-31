import { Card, CardContent, Typography, Grid } from "@mui/material";

const BacktestSummary = ({ summary }) => (
  <Card sx={{ mb: 2 }}>
    <CardContent>
      <Typography variant="h6">📊 Summary</Typography>
      <Grid container spacing={2}>
        {Object.entries(summary).map(([key, value]) => (
          <Grid item xs={6} sm={4} key={key}>
            <Typography variant="body2">
              {key.replace(/_/g, " ")}: <strong>{value}</strong>
            </Typography>
          </Grid>
        ))}
      </Grid>
    </CardContent>
  </Card>
);

export default BacktestSummary;
