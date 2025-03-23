const WS_BASE_URL = process.env.WEBSOCKET_BASE_URL;

export const connectWebSocket = (onMessage) => {
    const ws = new WebSocket(WS_BASE_URL);

    ws.onopen = () => console.log("✅ WebSocket Connected");
    ws.onmessage = (event) => onMessage(JSON.parse(event.data));
    ws.onclose = () => console.log("🔌 WebSocket Disconnected");

    return ws;
};
