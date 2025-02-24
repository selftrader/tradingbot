 const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
 // ✅ Load API URL from .env
 

export const signup = async (credentials) => {
  try {
    const response = await fetch(`${API_URL}/api/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    return response.ok ? { success: true } : { success: false, error: "Signup failed" };
  } catch (error) {
    return { success: false, error: "Server error" };
  }
};

export const login = async (credentials) => {
  try {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) return { success: false, error: "Invalid credentials" };

    const data = await response.json();
    localStorage.setItem("token", data.token);
    localStorage.setItem("isLoggedIn", "true");  // ✅ Store login state
    window.dispatchEvent(new Event("storage"));  // ✅ Notify all components of login

    return { success: true };
  } catch (error) {
    return { success: false, error: "Server error" };
  }
};

// ✅ Logout function clears everything properly
export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("isLoggedIn");
  window.dispatchEvent(new Event("storage"));  // ✅ Notify React components about logout
};

// ✅ Check if user is authenticated
export const isAuthenticated = () => !!localStorage.getItem("token");
