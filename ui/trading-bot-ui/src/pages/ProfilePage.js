import React, { useEffect, useState } from "react";
import { Card, CardContent, Avatar, Typography, Grid, CircularProgress, Box } from "@mui/material";
import apiClient from "../services/api";

const ProfilePage = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await apiClient.get("/user/profile"); // ✅ Fetch user profile
                setProfile(response.data);
            } catch (err) {
                console.error("Error fetching profile:", err);
                setError("Failed to load profile.");
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    if (loading) return <Box display="flex" justifyContent="center" mt={5}><CircularProgress /></Box>;
    if (error) return <p style={{ color: "red", textAlign: "center" }}>{error}</p>;

    return (
        <Grid container justifyContent="center" mt={5}>
            <Grid item xs={12} sm={8} md={6}>
                <Card sx={{ p: 3, boxShadow: 3 }}>
                    <Box display="flex" flexDirection="column" alignItems="center">
                        {/* Profile Picture */}
                        <Avatar
                            src={profile.avatar || "/assets/default-avatar.png"}
                            alt="Profile Picture"
                            sx={{ width: 100, height: 100, mb: 2 }}
                        />

                        {/* User Details */}
                        <Typography variant="h5" fontWeight="bold">
                            {profile.name}
                        </Typography>
                        <Typography variant="subtitle1" color="textSecondary">
                            {profile.email}
                        </Typography>
                    </Box>

                    <CardContent>
                        {/* Additional Profile Details */}
                        <Grid container spacing={2}>
                            {/* <Grid item xs={12} sm={6}>
                                <Typography variant="body1"><strong>Username:</strong> {profile.username}</Typography>
                            </Grid> */}
                            <Grid item xs={12} sm={6}>
                                <Typography variant="body1"><strong>Role:</strong> {profile.role || "User"}</Typography>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <Typography variant="body1"><strong>Phone:</strong> {profile.phone || "Not provided"}</Typography>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <Typography variant="body1"><strong>Country:</strong> {profile.country || "Not specified"}</Typography>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

export default ProfilePage;
