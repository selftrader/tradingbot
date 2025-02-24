import React, { useState, useEffect } from "react";
import { Container, Typography, TextField, Button, Box } from "@mui/material";
import { getUserProfile, updateUserProfile } from "../services/userService";

const ProfilePage = () => {
  const [user, setUser] = useState({ name: "", email: "" });
  const [newName, setNewName] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      const data = await getUserProfile();
      if (data) {
        setUser(data);
        setNewName(data.name);
      }
    };
    fetchProfile();
  }, []);

  const handleUpdate = async () => {
    const result = await updateUserProfile(newName);
    if (result.success) {
      setUser((prev) => ({ ...prev, name: newName }));
      alert("Profile updated successfully!");
    }
  };

  return (
    <Container sx={{ mt: 4, textAlign: "center" }}>
      <Typography variant="h4">User Profile</Typography>
      <Box sx={{ mt: 3 }}>
        <TextField
          label="Email"
          value={user.email}
          fullWidth
          disabled
          sx={{ mb: 2 }}
        />
        <TextField
          label="Name"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        />
        <Button variant="contained" color="primary" onClick={handleUpdate}>
          Update Profile
        </Button>
      </Box>
    </Container>
  );
};

export default ProfilePage;
