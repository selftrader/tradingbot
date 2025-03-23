import { useEffect, useState } from "react";

const BASE_URL = process.env.REACT_APP_API_URL;

function BacktestResults({ userId }) {
    const [results, setResults] = useState([]);

    useEffect(() => {
        fetch(`{BASE_URL}/api/backtest?user_id=${userId}`)
            .then(response => response.json())
            .then(data => setResults(data))
            .catch(error => console.error("Error fetching backtest results:", error));
    }, [userId]);

    return (
        <div>
            <h2>AI Backtest Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Trade Type</th>
                        <th>AI Confidence (%)</th>
                        <th>Actual Close</th>
                        <th>Result</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((entry, index) => (
                        <tr key={index}>
                            <td>{entry.symbol}</td>
                            <td>{entry.trade_type}</td>
                            <td>{entry.ai_confidence}%</td>
                            <td>₹{entry.actual_close}</td>
                            <td>{entry.result}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default BacktestResults;
