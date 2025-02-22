import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

export const subscribeToTradeUpdates = (callback) => {
    const intervalId = setInterval(() => {
        const update = {
            time: new Date().toLocaleTimeString(),
            message: "Simulated trade update"
        };
        callback(update);
    }, 5000); // simulate an update every 5 seconds
    
    // Return an unsubscribe function
    return () => clearInterval(intervalId);
};

export const analyzeSectoralOptions = async (sector) => {
    const response = await apiClient.get(`/analysis/sectoral/${sector}`);
    return response.data;
};

export const tradingAPI = {
    startTrading: async (stock) => {
        const response = await apiClient.post('/trading/start', { symbol: stock.symbol });
        return response.data;
    },

    stopTrading: async () => {
        const response = await apiClient.post('/trading/stop');
        return response.data;
    },

    saveConfiguration: async (config) => {
        const response = await apiClient.post('/trading/config', config);
        return response.data;
    },

    getConfiguration: async () => {
        const response = await apiClient.get('/trading/config');
        return response.data;
    },

    getAvailableStocks: async () => {
        const response = await apiClient.get('/stocks/available');
        return response.data;
    },

    // Get all available options stocks
    getOptionsStocks: async () => {
        const response = await apiClient.get('/stocks/options-available');
        return response.data;
    },

    // Get Nifty sectoral indices
    getSectoralIndices: async () => {
        const response = await apiClient.get('/market/sectoral-indices');
        return response.data;
    },

    // Get options chain for a specific stock
    getOptionsChain: async (symbol) => {
        const response = await apiClient.get(`/stocks/${symbol}/options-chain`);
        return response.data;
    },

    // Get AI analysis for a stock
    getStockAnalysis: async (symbol) => {
        const response = await apiClient.get(`/analysis/stock/${symbol}`);
        return response.data;
    },

    // Get AI-based stock recommendations
    getAIRecommendations: async (params) => {
        const response = await apiClient.get('/analysis/ai-recommendations', { params });
        return response.data;
    },

    // Get sector-specific stock analysis
    getSectorAnalysis: async (sector) => {
        const response = await apiClient.get(`/analysis/sector/${sector}`);
        return response.data;
    },

    // Add broker-related methods
    getBrokerConfig: async () => {
        const response = await apiClient.get('/broker/config');
        return response.data;
    },

    saveBrokerConfig: async (config) => {
        const response = await apiClient.post('/broker/configure', config);
        return response.data;
    },

    getTradeStatus: async (symbol) => {
        const response = await apiClient.get(`/broker/status/${symbol}`);
        return response.data;
    },

    getTrades: async (symbol) => {
        const response = await axios.get(`${BASE_URL}/trades?symbol=${symbol}`);
        return response.data;
    },

    getBrokerConfigs: async (params) => {
        const response = await apiClient.get('/brokers', { params });
        return response.data;
    },

    login: async (loginData) => {
        const response = await apiClient.post('/auth/login', loginData);
        return response.data;
    },

    signup: async (signupData) => {
        const response = await apiClient.post('/auth/signup', signupData);
        return response.data;
    }
};

// Add new constant for available sectors
export const NIFTY_SECTORS = {
    NIFTY50: 'NIFTY 50',
    BANKNIFTY: 'BANK NIFTY',
    FINNIFTY: 'FIN NIFTY',
    IT: 'NIFTY IT',
    PHARMA: 'NIFTY PHARMA',
    AUTO: 'NIFTY AUTO',
    FMCG: 'NIFTY FMCG'
};

// Add constant for stock categories
export const STOCK_CATEGORIES = {
    OPTIONS_ALLOWED: 'Options Allowed',
    FNO: 'F&O',
    CASH: 'Cash'
};

// Add websocket subscription for options data
export const subscribeToOptionsData = (symbol, callback) => {
    const ws = new WebSocket(
        `${process.env.REACT_APP_WS_URL || 'ws://localhost:8000'}/ws/options/${symbol}`
    );
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        callback(data);
    };

    return () => ws.close();
};

// Example response structure for getOptionsStocks:
/*
{
    stocks: [
        {
            symbol: "RELIANCE",
            name: "Reliance Industries Ltd",
            sector: "NIFTY50",
            optionsAllowed: true,
            lotSize: 250,
            lastPrice: 2500.50,
            change: 1.5
        },
        // ... more stocks
    ]
}
*/

// Example response structure for getAIRecommendations:
/*
{
    recommendations: [
        {
            symbol: "HDFCBANK",
            confidence: 0.85,
            action: "BUY",
            strategy: "BULL_CALL_SPREAD",
            analysis: {
                technicalScore: 8.5,
                fundamentalScore: 7.8,
                marketSentiment: "Bullish",
                volatility: "Medium"
            }
        },
        // ... more recommendations
    ]
}
*/


export const fetchLiveUpdates = async () => {
    try {
      const response = await fetch(`${BASE_URL}/live-updates`);
      if (!response.ok) throw new Error("Failed to fetch live updates");
      return await response.json();
    } catch (error) {
      console.error("Error fetching live updates:", error);
      return [];
    }
  };
  
  export const fetchConfig = async () => {
    try {
      const response = await fetch(`${BASE_URL}/config`);
      if (!response.ok) throw new Error("Failed to fetch config");
      return await response.json();
    } catch (error) {
      console.error("Error fetching config:", error);
      return null;
    }
  };

export default tradingAPI;