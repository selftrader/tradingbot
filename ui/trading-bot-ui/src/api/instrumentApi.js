import axios from "axios";

export const searchStocks = async (query) =>
  axios.get(`/api/instruments/search?q=${query}`);

export const fetchOptionChain = async (symbol, range) =>
  axios.get(`/api/instruments/chain?symbol=${symbol}&range=${range}`);
