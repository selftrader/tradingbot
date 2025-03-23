import { useEffect, useState } from "react";
const WS_BASE_URL = process.env.REACT_APP_API_URL;
function LiveAI({ userId }) {
    const [aiDecisions, setAIDecisions] = useState([]);

    useEffect(() => {
        const socket = new WebSocket(`ws://{WS_BASE_URL}/ws/ai_decisions?user_id=${userId}`);

        socket.onmessage = (event) => {
            setAIDecisions(JSON.parse(event.data));
        };

        return () => socket.close();
    }, [userId]);

    return (
        <div>
            <h2>Live AI Trading Decisions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>AI Status</th>
                    </tr>
                </thead>
                <tbody>
                    {aiDecisions.map((decision, index) => (
                        <tr key={index}>
                            <td>{decision.symbol}</td>
                            <td>{decision.ai_status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default LiveAI;
