import React, { useEffect, useRef } from "react";

const TradingViewChart = ({ symbol, exchange }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!symbol) return;

    if (exchange === "NSE") {
      containerRef.current.innerHTML = `<iframe src="https://charting.nseindia.com/?symbol=${symbol}-EQ"
        width="100%" height="400px" frameborder="0" allowfullscreen></iframe>`;
    } else {
      const script = document.createElement("script");
      script.src = "https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js";
      script.async = true;
      script.innerHTML = JSON.stringify({
        symbol: `BSE:${symbol}`,
        width: "100%",
        height: 400,
        locale: "en",
        colorTheme: "dark",
        autosize: true,
      });

      if (containerRef.current) {
        containerRef.current.innerHTML = "";
        containerRef.current.appendChild(script);
      }
    }
  }, [symbol, exchange]);

  return <div ref={containerRef} />;
};

export default TradingViewChart;
