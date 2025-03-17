import apiClient from "./api";  // ✅ Use centralized API client

const tradingAPI = {
    startTrading: async (symbol) => {
        const response = await apiClient.post("/trading/start", { symbol });
        return response.data;
    },

    stopTrading: async () => {
        const response = await apiClient.post("/trading/stop");
        return response.data;
    },

    getStockAnalysis: async (symbol) => {
        const response = await apiClient.get(`/analysis/stock/${symbol}`);
        return response.data;
    }
};

export default tradingAPI;
