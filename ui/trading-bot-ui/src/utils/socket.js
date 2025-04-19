let socket = null;

export const getSocket = (url) => {
  if (
    !socket ||
    socket.readyState === WebSocket.CLOSED ||
    socket.readyState === WebSocket.CLOSING
  ) {
    socket = new WebSocket(url);
  }
  return socket;
};

export const closeSocket = () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close();
  }
  socket = null;
};
