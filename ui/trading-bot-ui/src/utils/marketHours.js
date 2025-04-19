export const isMarketOpen = () => {
  const now = new Date();
  const day = now.getDay();
  const hours = now.getHours();
  const minutes = now.getMinutes();

  // Market is open Mon–Fri 9:15AM to 3:30PM IST
  if (day === 0 || day === 6) return false;
  if (hours < 9 || (hours === 9 && minutes < 15)) return false;
  if (hours > 15 || (hours === 15 && minutes > 30)) return false;

  return true;
};
