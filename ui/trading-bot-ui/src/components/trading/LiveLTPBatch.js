import { useEffect, useRef, useState, useCallback } from "react";
const REACT_APP_WS_URL = process.env.REACT_APP_WS_URL;
const LiveLTPBatch = ({ stocks, updateLTPs }) => {
  const wsRef = useRef(null);
  const [connectionStatus, setConnectionStatus] = useState("disconnected");
  const lastSentKeys = useRef([]);

  const getInstrumentKeys = useCallback(() => {
    return stocks.map((s) => s.instrumentKey).sort();
  }, [stocks]);

  const sendSubscription = (instrumentKeys) => {
    if (
      wsRef.current &&
      wsRef.current.readyState === WebSocket.OPEN &&
      instrumentKeys.length
    ) {
      wsRef.current.send(JSON.stringify({ data: { instrumentKeys } }));
      lastSentKeys.current = instrumentKeys;
      console.log("📨 Sent subscription:", instrumentKeys);
    }
  };

  const connectWebSocket = useCallback(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    const socket = new WebSocket(
      `${REACT_APP_WS_URL}/ws/market?token=${token}`
    );
    wsRef.current = socket;

    socket.onopen = () => {
      setConnectionStatus("connected");
      const keys = getInstrumentKeys();
      sendSubscription(keys);
    };

    socket.onmessage = async (event) => {
      const raw =
        typeof event.data === "string" ? event.data : await event.data.text();
      const message = JSON.parse(raw);

      if (message.error) {
        setConnectionStatus("error");
        console.error("❌ Server Error:", message.error);
        return;
      }

      if (message.status === "connected") {
        console.log("✅ WebSocket Handshake OK");
        return;
      }

      if (message.event === "market_closed") {
        setConnectionStatus("closed");
        socket.close();
        return;
      }

      if (message.instrument_key && message.data) {
        updateLTPs({
          [message.instrument_key]: message.data,
        });
      }
    };

    socket.onclose = () => {
      setConnectionStatus("disconnected");
    };
  }, [getInstrumentKeys, updateLTPs]);

  // 👉 Open only once
  useEffect(() => {
    connectWebSocket();
    return () => wsRef.current?.close();
  }, [connectWebSocket]);

  // 👉 Detect new stock additions
  useEffect(() => {
    const currentKeys = getInstrumentKeys();
    const diffKeys = currentKeys.filter(
      (key) => !lastSentKeys.current.includes(key)
    );
    if (diffKeys.length > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
      sendSubscription(currentKeys);
    }
  }, [stocks, getInstrumentKeys]);

  return (
    <div>
      <strong>Status:</strong>{" "}
      <span className={connectionStatus}>{connectionStatus}</span>
    </div>
  );
};

export default LiveLTPBatch;
