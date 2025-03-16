import { refreshAccessToken } from "./authService"; // ✅ Import from authService.js

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
// ✅ Fetch User Profile
export const getUserProfile = async () => {
    try {
        let token = localStorage.getItem("access_token");

        if (!token) {
            console.warn("User is not logged in, no token found.");
            return { success: false, error: "Unauthorized: No token found." };
        }

        const response = await fetch(`${API_URL}/api/user/profile`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        if (response.status === 401) {
            console.warn("⚠️ Access token expired, attempting refresh...");

            const newToken = await refreshAccessToken();
            if (!newToken) {
                return { success: false, error: "Session expired. Please log in again." };
            }

            // ✅ Retry request with new token
            return await getUserProfile();
        }

        if (!response.ok) {
            const errorMessage = `API Error: ${response.status} ${response.statusText}`;
            console.error(errorMessage);
            return { success: false, error: errorMessage };
        }

        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        console.error("❌ Failed to fetch user profile:", error);
        return { success: false, error: "Server error" };
    }
};



export const getAuthToken = () => {
    const token = localStorage.getItem("accessToken");

    if (!token || token === "undefined") {
        console.warn("🔴 No valid token found in localStorage");
        return null;
    }
    return token;
};