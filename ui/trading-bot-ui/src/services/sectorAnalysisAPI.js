import apiClient from "./api";  // ✅ Use centralized API client

export const analyzeSectoralOptions = async (sector) => {
    try {
        const response = await apiClient.get(`/analysis/sectoral/${sector}`);
        return response.data;
    } catch (error) {
        console.error("❌ Failed to analyze sector:", error);
        throw error;
    }
};
