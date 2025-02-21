import React from "react";

function TradeTable({ trades }) {
  return (
    <div>
      <h3>Executed Trades</h3>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Action</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((trade, index) => (
            <tr key={index}>
              <td>{trade.symbol}</td>
              <td>{trade.action}</td>
              <td>{trade.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TradeTable;
