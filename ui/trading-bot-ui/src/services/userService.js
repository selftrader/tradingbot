const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const getUserProfile = async () => {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const response = await fetch(`${API_URL}/user/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      console.error("Failed to fetch user profile");
      return null;
    }

    const data = await response.json();
    
    // ✅ Ensure avatar field exists
    return {
      ...data,
      avatar: data.avatar || "/assets/default-avatar.png",  // Fallback image
    };
  } catch (error) {
    console.error("Error fetching user profile:", error);
    return null;
  }
};

export const updateUserProfile = async (name) => {
  const token = localStorage.getItem("token");
  if (!token) return { success: false };

  const response = await fetch(`${API_URL}/user/profile`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name }),
  });

  return response.ok ? { success: true } : { success: false };
};
