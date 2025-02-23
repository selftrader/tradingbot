
const API_URL = process.env.API_URL// ✅ Load API from .env


export const fetchStockList = async (exchange) => {
    try {
      const apiUrl = exchange === "NSE"
        ? `https://charting.nseindia.com/api/equity-stockIndices?index=NIFTY%2050`
        : `https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w?flag=5&sid=1`;
  
      const response = await fetch(apiUrl, {
        headers: { "User-Agent": "Mozilla/5.0" }
      });
  
      if (!response.ok) throw new Error("Failed to fetch stock list");
  
      const data = await response.json();
      return exchange === "NSE"
        ? data.data.map((item) => ({ symbol: item.symbol }))
        : data.map((item) => ({ symbol: item.scrip_cd }));
    } catch (error) {
      console.error("Error fetching stock list:", error);
      return [];
    }
  };
  
  // 🔹 FIXED: Added `fetchStockData` function to fetch live stock prices

export const fetchStockData = async ({ symbol, exchange }) => {
  try {
    const response = await fetch(`${API_URL}/api/stock/${symbol}/${exchange}`);

    if (!response.ok) {
      throw new Error(`Failed to fetch stock data: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching stock data:", error);
    return null;
  }
};
