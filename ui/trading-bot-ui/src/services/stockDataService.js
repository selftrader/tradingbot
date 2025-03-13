import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const searchStocks = async (query) => {
    try {
        const response = await axios.get(`${BASE_URL}/search-stocks?q=${query}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching stocks:", error);
        return [];
    }
};
