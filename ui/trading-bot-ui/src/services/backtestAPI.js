import apiClient from './api';

const backtestAPI = {
  runBacktest: async (payload) => {
    const response = await apiClient.post("/backtest/run", payload);
    return response.data;
  }
};

export default backtestAPI;
