import React from "react";
import { Container, Typography, Paper, Avatar, List, ListItem, ListItemText } from "@mui/material";

const ProfilePage = () => {
  // Sample user data (Replace with API call later)
  const user = {
    name: "John Doe",
    email: "johndoe@example.com",
    tradingReports: ["Trade 1 - Profit: $500", "Trade 2 - Loss: $200", "Trade 3 - Profit: $300"],
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4, textAlign: "center" }}>
        <Avatar sx={{ width: 80, height: 80, margin: "auto" }} alt="Profile Picture" src="/path/to/profile-pic.jpg" />
        <Typography variant="h5" sx={{ mt: 2 }}>{user.name}</Typography>
        <Typography variant="subtitle1" color="textSecondary">{user.email}</Typography>

        <Typography variant="h6" sx={{ mt: 4 }}>Trading Reports</Typography>
        <List>
          {user.tradingReports.map((report, index) => (
            <ListItem key={index}>
              <ListItemText primary={report} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
};

export default ProfilePage;
