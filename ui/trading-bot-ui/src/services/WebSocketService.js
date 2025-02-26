import { io } from 'socket.io-client';

// ✅ Load WebSocket URL from .env or use default localhost
const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:8000';

// ✅ Validate WebSocket URL
if (!process.env.REACT_APP_SOCKET_URL) {
    console.warn("⚠️ Warning: REACT_APP_SOCKET_URL is not set. Using default localhost.");
}

// ✅ Initialize WebSocket connection
const socket = io(SOCKET_URL, {
    transports: ['websocket'],
    reconnectionAttempts: 5,  // ✅ Retry 5 times if connection fails
    timeout: 5000             // ✅ Wait 5 sec before timing out
});

// ✅ WebSocket event handlers
socket.on('connect', () => {
    console.log("✅ WebSocket Connected:", SOCKET_URL);
});

socket.on('disconnect', (reason) => {
    console.warn("⚠️ WebSocket Disconnected:", reason);
});

socket.on('trade_update', (data) => {
    console.log("📈 Live Trade Update:", data);
});

export default socket;
