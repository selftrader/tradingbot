import React, { useState, useEffect } from "react";

function AIStatus() {
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    fetch("http://localhost:8000/api/status")
      .then((res) => res.json())
      .then((data) => setStatus(data.message));
  }, []);

  return <h3>AI Model Status: {status}</h3>;
}

export default AIStatus;
