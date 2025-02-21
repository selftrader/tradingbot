import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Trading API endpoints
export const tradingAPI = {
    // Bot control
    startBot: async (symbols) => {
        const response = await apiClient.post('/trading/start', { symbols });
        return response.data;
    },

    stopBot: async () => {
        const response = await apiClient.post('/trading/stop');
        return response.data;
    },

    getBotStatus: async () => {
        const response = await apiClient.get('/trading/status');
        return response.data;
    },

    // Stock data
    getAvailableStocks: async () => {
        const response = await apiClient.get('/stocks/available');
        return response.data;
    },

    // Trading configuration
    saveTradingConfig: async (config) => {
        const response = await apiClient.post('/trading/config', config);
        return response.data;
    },

    getTradingConfig: async () => {
        const response = await apiClient.get('/trading/config');
        return response.data;
    },

    // Trading history
    getTradingHistory: async (params) => {
        const response = await apiClient.get('/trading/history', { params });
        return response.data;
    },

    // Market data
    getLiveQuote: async (symbol) => {
        const response = await apiClient.get(`/market/quote/${symbol}`);
        return response.data;
    },

    getMarketStatus: async () => {
        const response = await apiClient.get('/market/status');
        return response.data;
    },

};

// Error interceptor
apiClient.interceptors.response.use(
    response => response,
    error => {
        const errorMessage = error.response?.data?.message || 'An error occurred';
        console.error('API Error:', errorMessage);
        return Promise.reject(error);
    }
);




export default tradingAPI;
