const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ✅ Signup API Call
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

// ✅ Login API Call (Sends email instead of username)
export const login = async ({ email, password }) => {
  try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),  // ✅ Send email, NOT username
      });

      if (!response.ok) return { success: false, error: "Invalid credentials" };

      const data = await response.json();
      localStorage.setItem("token", data.token);
      localStorage.setItem("isLoggedIn", "true");  // ✅ Store login state
      window.dispatchEvent(new Event("storage"));  // ✅ Notify React components

      return { success: true };
  } catch (error) {
      return { success: false, error: "Server error" };
  }
};

// ✅ Logout Function
export const logout = () => {
    console.log("✅ Logout function called!");

    // ✅ Clear authentication data
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");

    // ✅ Redirect to Landing Page (`/`)
    window.location.href = "/";  
};

// ✅ Check if user is authenticated
export const isAuthenticated = () => !!localStorage.getItem("token");
