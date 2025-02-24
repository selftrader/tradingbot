const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const getUserProfile = async () => {
  const token = localStorage.getItem("token");
  if (!token) return null;

  const response = await fetch(`${API_URL}/profile`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  return response.ok ? await response.json() : null;
};

export const updateUserProfile = async (name) => {
  const token = localStorage.getItem("token");
  if (!token) return { success: false };

  const response = await fetch(`${API_URL}/profile`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name }),
  });

  return response.ok ? { success: true } : { success: false };
};
