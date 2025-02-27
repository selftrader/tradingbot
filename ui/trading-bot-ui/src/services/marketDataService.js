export const fetchMarketData = async (symbol) => {
    try {
      const response = await fetch(`https://api.example.com/marketdata?symbol=${symbol}`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching market data:", error);
      return null;
    }
  };


  export const fetchStockList = async (exchange, instrument) => {
    try {
      const response = await fetch(`/api/stocks?exchange=${exchange}&instrument=${instrument}`);
      const data = await response.json();
      
      // ✅ Ensure API response has correct structure
      if (!data.stocks || !Array.isArray(data.stocks)) {
        console.error("Invalid stock list response:", data);
        return [];
      }
  
      return data.stocks.map(stock => ({ symbol: stock.symbol || stock.name })); // ✅ Ensure symbol exists
    } catch (error) {
      console.error("Error fetching stock list:", error);
      return [];
    }
  };


  export const fetchLiveStockPrice = async (symbol) => {
    try {
      const response = await fetch(`/api/stock-price?symbol=${symbol}`);
      const data = await response.json();
      return data.price; // ✅ Returns live stock price
    } catch (error) {
      console.error("Error fetching live price:", error);
      return 0;
    }
  };
  