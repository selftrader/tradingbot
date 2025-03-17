import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

const apiClient = axios.create({
    baseURL: BASE_URL,
    headers: { "Content-Type": "application/json" },
    withCredentials: true, // ✅ Required for CORS authentication
});

// ✅ Attach access token to API requests
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// ✅ Handle 401 Unauthorized and refresh token automatically
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        console.error("📌 Axios Error:", error);

        if (!error.response) {
            console.error("🚨 Network Error: Server Unreachable");
            return Promise.reject({
                code: "ERR_NETWORK",
                message: "Unable to connect to the server. Please check your internet or backend server.",
            });
        }

        const originalRequest = error.config;

        if (error.response.status === 401 && error.response.data?.code === "token_expired") {
            console.warn("🚨 Access token expired, attempting to refresh...");

            const refreshToken = localStorage.getItem("refresh_token");
            if (!refreshToken) {
                console.error("❌ Refresh token missing, logging out user.");
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                window.location.href = "/";
                return Promise.reject(error);
            }

            try {
                const refreshResponse = await axios.post(
                    `${BASE_URL}/refresh-token`,
                    {},
                    { headers: { "Refresh-Token": refreshToken } }
                );

                if (refreshResponse.status === 200) {
                    const newAccessToken = refreshResponse.data.access_token;
                    console.log("🔄 Token refreshed successfully");

                    localStorage.setItem("access_token", newAccessToken);

                    // ✅ Retry the failed request with the new token
                    originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
                    return apiClient(originalRequest);
                } else {
                    throw new Error("Refresh token invalid");
                }
            } catch (refreshError) {
                console.error("❌ Token refresh failed:", refreshError);
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                window.location.href = "/login";
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;
