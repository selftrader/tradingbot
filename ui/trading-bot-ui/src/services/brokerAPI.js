import apiClient from "./api";  // ✅ Use centralized API client

const brokerAPI = {
    getBrokers: async () => {
        const response = await apiClient.get("/broker/list");
        return response.data;
    },

    deleteBroker: async (id) => {
        const response = await apiClient.delete(`/broker/delete/${id}`);
        return response.data;
    },

    addBroker: async (brokerData) => {
        const response = await apiClient.post("/broker/add", brokerData);
        return response.data;
    },

    initUpstoxAuth: async (credentials) => {
        const response = await apiClient.post("/broker/upstox/init-auth", credentials);
        return response.data;
      },

    initFyersAuth: async (payload) => {
        const response = await apiClient.post("/broker/fyers/init-auth", payload);
        return response.data;
    },
    
    
};

export default brokerAPI;
