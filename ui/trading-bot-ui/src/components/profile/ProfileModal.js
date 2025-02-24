import React, { useState, useEffect } from "react";
import { Dialog, DialogTitle, DialogContent, TextField, Button, Box } from "@mui/material";
import { getUserProfile, updateUserProfile } from "../../services/userService";

const ProfileModal = ({ open, onClose }) => {
  const [user, setUser] = useState({ name: "", email: "" });
  const [newName, setNewName] = useState("");

  useEffect(() => {
    if (open) {
      const fetchProfile = async () => {
        const data = await getUserProfile();
        if (data) {
          setUser(data);
          setNewName(data.name);
        }
      };
      fetchProfile();
    }
  }, [open]);

  const handleUpdate = async () => {
    const result = await updateUserProfile(newName);
    if (result.success) {
      setUser((prev) => ({ ...prev, name: newName }));
      alert("Profile updated successfully!");
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>User Profile</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <TextField label="Email" value={user.email} fullWidth disabled sx={{ mb: 2 }} />
          <TextField label="Name" value={newName} onChange={(e) => setNewName(e.target.value)} fullWidth sx={{ mb: 2 }} />
          <Button variant="contained" color="primary" onClick={handleUpdate}>Update Profile</Button>
        </Box>
      </DialogContent>
    </Dialog>
  );
};

export default ProfileModal;
