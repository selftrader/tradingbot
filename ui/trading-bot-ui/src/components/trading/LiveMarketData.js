import React, { useState, useEffect, useCallback } from "react";
import { Card, Table, Alert } from "antd";
import { useAuth } from "../../contexts/AuthContext";
import { formatNumber } from "../../utils/formatters";

const REACT_APP_WS_URL = process.env.REACT_APP_WS_URL;

const LiveMarketData = ({ instrumentKeys = [] }) => {
  const [marketData, setMarketData] = useState({});
  const [error, setError] = useState(null);
  const [wsStatus, setWsStatus] = useState("disconnected");
  const { token } = useAuth();

  const connectWebSocket = useCallback(() => {
    if (!token || instrumentKeys.length === 0) return;

    const ws = new WebSocket(`${REACT_APP_WS_URL}/ws/market?token=${token}`);

    ws.onopen = () => {
      setWsStatus("connected");
      setError(null);

      // Send subscription message
      ws.send(
        JSON.stringify({
          data: {
            instrumentKeys: instrumentKeys,
          },
        })
      );
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          return;
        }

        if (data.instrument_key && data.data) {
          setMarketData((prev) => ({
            ...prev,
            [data.instrument_key]: {
              ...data.data,
              lastUpdate: new Date().toLocaleTimeString(),
            },
          }));
        }
      } catch (e) {
        console.error("Error processing message:", e);
      }
    };

    ws.onclose = () => {
      setWsStatus("disconnected");
      // Attempt to reconnect after 5 seconds
      setTimeout(connectWebSocket, 5000);
    };

    ws.onerror = (error) => {
      setError("WebSocket error occurred");
      console.error("WebSocket error:", error);
    };

    // Keep-alive ping
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send("ping");
      }
    }, 30000);

    // Cleanup on unmount
    return () => {
      clearInterval(pingInterval);
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [token, instrumentKeys]);

  useEffect(() => {
    const cleanup = connectWebSocket();
    return cleanup;
  }, [connectWebSocket]);

  const columns = [
    {
      title: "Instrument",
      dataIndex: "instrument",
      key: "instrument",
      render: (text) => {
        const parts = text.split("|");
        return parts[1] || text;
      },
    },
    {
      title: "LTP",
      dataIndex: "ltp",
      key: "ltp",
      render: (value) => formatNumber(value, 2),
    },
    {
      title: "Volume",
      dataIndex: "volume",
      key: "volume",
      render: (value) => formatNumber(value, 0),
    },
    {
      title: "Avg Price",
      dataIndex: "avg_price",
      key: "avg_price",
      render: (value) => formatNumber(value, 2),
    },
    {
      title: "Last Update",
      dataIndex: "lastUpdate",
      key: "lastUpdate",
    },
  ];

  const dataSource = Object.entries(marketData).map(([key, value]) => ({
    key,
    instrument: key,
    ...value,
  }));

  return (
    <Card
      title="Live Market Data"
      extra={
        <span
          style={{
            color: wsStatus === "connected" ? "#52c41a" : "#ff4d4f",
          }}
        >
          {wsStatus === "connected" ? "● Connected" : "● Disconnected"}
        </span>
      }
    >
      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        size="small"
        scroll={{ y: 400 }}
      />
    </Card>
  );
};

export default LiveMarketData;
