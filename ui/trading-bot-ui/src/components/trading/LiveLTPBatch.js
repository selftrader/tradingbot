// import { useEffect, useRef, useState, useCallback } from "react";

// const REACT_APP_WS_URL = process.env.REACT_APP_WS_URL;

// const LiveLTPBatch = ({ stocks, updateLTPs, setMarketOpen }) => {
//   const wsRef = useRef(null);
//   const reconnectTimerRef = useRef(null);
//   const lastSentKeys = useRef([]);
//   const [connectionStatus, setConnectionStatus] = useState("disconnected");

//   const getInstrumentKeys = useCallback(() => {
//     return stocks
//       .map((s) => s.instrument_key || s.instrumentKey)
//       .filter(Boolean)
//       .sort();
//   }, [stocks]);

//   const sendSubscription = (instrumentKeys) => {
//     if (
//       wsRef.current &&
//       wsRef.current.readyState === WebSocket.OPEN &&
//       instrumentKeys.length
//     ) {
//       const payload = {
//         data: { instrumentKeys },
//       };
//       wsRef.current.send(JSON.stringify(payload));
//       console.log("✅ Sent instrumentKeys to backend:", instrumentKeys);
//       lastSentKeys.current = instrumentKeys;
//     }
//   };

//   const connectWebSocket = useCallback(() => {
//     const token = localStorage.getItem("access_token");

//     if (!token) {
//       console.error("⛔ No access token found.");
//       setConnectionStatus("error");
//       return;
//     }

//     const socket = new WebSocket(
//       `${REACT_APP_WS_URL}/ws/market?token=${token}`
//     );
//     wsRef.current = socket;

//     socket.onopen = () => {
//       console.log("🔌 WebSocket connected");
//       setConnectionStatus("connected");
//       sendSubscription(getInstrumentKeys());
//     };

//     socket.onmessage = async (event) => {
//       const raw =
//         typeof event.data === "string" ? event.data : await event.data.text();

//       let message;
//       try {
//         message = JSON.parse(raw);
//       } catch (err) {
//         console.warn("🔍 Invalid JSON message:", raw);
//         return;
//       }

//       if (message?.error) {
//         console.error("❌ WebSocket error:", message.error);
//         setConnectionStatus("error");

//         if (message.error.toLowerCase().includes("expired")) {
//           alert("Session expired. Please login again.");
//           localStorage.removeItem("access_token");
//         }

//         socket.close();
//         return;
//       }

//       if (message?.event === "market_closed") {
//         console.warn("📴 Market closed by backend.");
//         setConnectionStatus("closed");
//         setMarketOpen(false);
//         socket.close();
//         return;
//       }

//       if (message?.type === "ltp_update" && message.data?.instrumentKey) {
//         updateLTPs({ [message.data.instrumentKey]: message.data });
//       }
//     };

//     socket.onerror = (err) => {
//       console.error("⚠️ WebSocket error:", err);
//       setConnectionStatus("error");
//     };

//     socket.onclose = () => {
//       console.warn("🔌 WebSocket disconnected");
//       setConnectionStatus("disconnected");

//       // ❌ Don't reconnect if market is closed
//       if (connectionStatus !== "closed") {
//         reconnectTimerRef.current = setTimeout(() => {
//           console.log("♻️ Reconnecting WebSocket...");
//           connectWebSocket();
//         }, 3000);
//       }
//     };
//   }, [getInstrumentKeys, updateLTPs, setMarketOpen, connectionStatus]);

//   useEffect(() => {
//     connectWebSocket();

//     return () => {
//       clearTimeout(reconnectTimerRef.current);
//       wsRef.current?.close();
//     };
//   }, [connectWebSocket]);

//   useEffect(() => {
//     const keys = getInstrumentKeys();
//     const hasChanged =
//       JSON.stringify(keys) !== JSON.stringify(lastSentKeys.current);

//     if (hasChanged && wsRef.current?.readyState === WebSocket.OPEN) {
//       sendSubscription(keys);
//     }
//   }, [stocks, getInstrumentKeys]);

//   return (
//     <div style={{ marginTop: 10 }}>
//       <small>
//         <strong>WS Status:</strong>{" "}
//         <span
//           style={{
//             color:
//               connectionStatus === "connected"
//                 ? "green"
//                 : connectionStatus === "closed"
//                 ? "orange"
//                 : "red",
//           }}
//         >
//           {connectionStatus === "connected"
//             ? "Live"
//             : connectionStatus === "closed"
//             ? "Market Closed"
//             : "Disconnected"}
//         </span>
//       </small>
//     </div>
//   );
// };

// export default LiveLTPBatch;
