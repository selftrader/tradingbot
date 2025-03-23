import { useEffect, useState } from "react";
const BASE_URL = process.env.REACT_APP_API_URL;
function AIPerformance({ userId }) {
    const [performance, setPerformance] = useState({});

    useEffect(() => {
         
        fetch(`{BASE_URL}/api/ai_performance?user_id=${userId}`)
            .then(response => response.json())
            .then(data => setPerformance(data))
            .catch(error => console.error("Error fetching AI performance:", error));
    }, [userId]);

    return (
        <div>
            <h2>AI Trading Performance</h2>
            <p>Total Trades: {performance.total_trades}</p>
            <p>AI Win Rate: {performance.win_rate}%</p>
            <p>AI Returns: {performance.AI_Returns}%</p>
            <p>Market Returns (NIFTY 50): {performance.Market_Returns}%</p>
        </div>
    );
}

export default AIPerformance;
