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