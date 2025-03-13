const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// ✅ Fetch User Profile
export const getUserProfile = async () => {
  try {
      const token = localStorage.getItem("access_token");

      if (!token) {
          console.warn("User is not logged in, no token found.");
          return { success: false, error: "Unauthorized: No token found." };
      }

      const response = await fetch(`${API_URL}/api/user/profile`, {
          method: "GET",
          headers: {
              "Authorization": `Bearer ${token}`,  // ✅ Send token correctly
              "Content-Type": "application/json",
          },
      });

      if (!response.ok) {
          const errorMessage = `API Error: ${response.status} ${response.statusText}`;
          console.error(errorMessage);
          return { success: false, error: errorMessage };
      }

      const data = await response.json();
      return { success: true, data };
  } catch (error) {
      console.error("Failed to fetch user profile:", error);
      return { success: false, error: "Server error" };
  }
};


//  Update User Profile
export const updateUserProfile = async (name) => {
    try {
        const token = localStorage.getItem("access_token"); // ✅ Use consistent key

        if (!token) {
            console.warn("User is not logged in, no token found.");
            return { success: false, error: "Unauthorized: No token found." };
        }

        const response = await fetch(`${API_URL}/api/user/profile`, {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name }),
        });

        if (!response.ok) {
            const errorMessage = `API Error: ${response.status} ${response.statusText}`;
            console.error(errorMessage);
            return { success: false, error: errorMessage };
        }

        return { success: true };
    } catch (error) {
        console.error("Failed to update user profile:", error);
        return { success: false, error: "Server error" };
    }
};
