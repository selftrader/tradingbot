import { refreshAccessToken, logout } from "./authService"; // ✅ Import logout

const API_URL = process.env.REACT_APP_API_URL ;

// ✅ Fetch User Profile
export const getUserProfile = async () => {
    let token = localStorage.getItem("access_token");

    if (!token) {
        return { success: false, error: "Unauthorized: No token" };
    }

    try {
        const response = await fetch(`${API_URL}/api/user/profile`, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        if (response.status === 401) {
            const newToken = await refreshAccessToken();
            if (!newToken) {
                logout(); // ✅ Now imported
                return { success: false, error: "Session expired" };
            }

            // ✅ Retry with new token
            return await getUserProfile();
        }

        if (!response.ok) {
            return { success: false, error: "API error" };
        }

        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        console.error("User profile fetch failed:", error);
        return { success: false, error: "Server error" };
    }
};
