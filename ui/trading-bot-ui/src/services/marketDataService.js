const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const fetchMarketData = async (symbol) => {
    try {
        const response = await fetch(`${API_URL}/marketdata?symbol=${symbol}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching market data:", error);
        return null;
    }
};

export const fetchStockList = async (exchange, instrument) => {
    try {
        const response = await fetch(`${API_URL}/api/stocks/search?exchange=${exchange}&instrument=${instrument}`);

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error fetching stock list:", error);
        return [];
    }
};

export const fetchLiveStockPrice = async (symbol) => {
    try {
        const response = await fetch(`${API_URL}/api/stock-price?symbol=${symbol}`);
        const data = await response.json();
        return data.price; // ✅ Returns live stock price
    } catch (error) {
        console.error("Error fetching live price:", error);
        return 0;
    }
};
