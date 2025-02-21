import React from "react";

function BotLogs({ logs }) {
  return (
    <div>
      <h3>Bot Activity Logs</h3>
      <ul>
        {logs.map((log, index) => (
          <li key={index}>{log.message}</li>
        ))}
      </ul>
    </div>
  );
}

export default BotLogs;
