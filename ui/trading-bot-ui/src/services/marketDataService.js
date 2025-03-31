import apiClient from "./api";
const API_URL = process.env.REACT_APP_API_URL;

// ✅ NEW: Fetch stock snapshot for dashboard (cleaner and safer)
export const fetchStockSnapshot = async (symbol) => {
  try {
    const response = await apiClient.get(`/api/market-data/stock/snapshot`, {
      params: { symbol },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching stock snapshot:", error);
    return null;
  }
};

// (Optional: Keep the rest if still used somewhere else)
export const fetchStockList = async (exchange, instrument) => {
  try {
    const response = await fetch(
      `${API_URL}/api/stocks/search?exchange=${exchange}&instrument=${instrument}`
    );
    if (!response.ok) throw new Error(`API Error: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching broker instruments:", error);
    return [];
  }
};

export const fetchLiveStockPrice = async (symbol, exchange, instrument) => {
  try {
    const response = await apiClient.get(`/live-price`, {
      params: { symbol, exchange, instrument },
    });
    return response.data.price;
  } catch (error) {
    console.error("Error fetching live price:", error);
    return 0;
  }
};

// Reuse this for resolve call
export const resolveStockDetails = async (symbol, exchange) => {
  try {
    const response = await apiClient.get(`${API_URL}/api/stocks/resolve`, {
      params: { symbol, exchange },
    });

    if (response.status === 200) {
      return response.data;
    } else {
      console.warn("No data returned for stock resolve");
      return null;
    }
  } catch (error) {
    console.error(
      "Failed to resolve stock details:",
      error?.response?.data || error.message
    );
    return null;
  }
};
