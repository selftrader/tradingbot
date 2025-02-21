import React from "react";
import TradeTable from "./TradeTable";
import AIStatus from "./AIStatus";
import BotLogs from "./BotLogs";

function Dashboard({ trades, botLogs }) {
  return (
    <div>
      <h2>AI Trading Dashboard</h2>
      <AIStatus />
      <BotLogs logs={botLogs} />
      <TradeTable trades={trades} />
    </div>
  );
}

export default Dashboard;
