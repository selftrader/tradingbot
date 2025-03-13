const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ✅ Signup API Call
export const signup = async (credentials) => {
    try {
        const response = await fetch(`${API_URL}/api/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentials),
        });

        const data = await response.json();

        if (!response.ok) {
            return { 
                success: false, 
                message: Array.isArray(data.detail?.errors) 
                    ? data.detail.errors.join(", ")  // ✅ Properly format multiple errors
                    : "Signup failed"
            };
        }

        return { success: true, message: "Signup successful" };
    } catch (error) {
        return { success: false, message: "Server error. Please try again later." };
    }
};

// ✅ OTP Verification API Call
export const verifyOtp = async (phone, countryCode, otp) => {
    try {
        const response = await fetch(`${API_URL}/api/auth/verify-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phone_number: phone, country_code: countryCode, otp }),
        });

        const data = await response.json();

        if (!response.ok) {
            return { 
                success: false, 
                message: data.detail === "OTP has expired. Please request a new one."
                    ? "Your OTP has expired. Please request a new one."
                    : data.detail || "OTP verification failed."
            };
        }

        return { success: true, message: data.message };
    } catch (error) {
        return { success: false, message: "Server error. Please try again later." };
    }
};

export const resendOtp = async (phone_number, country_code,otp) => {
    try {
        const response = await fetch("/api/auth/resend-otp", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ phone_number, country_code }),
        });

        return await response.json();
    } catch (error) {
        console.error("Resend OTP Error:", error);
        return { success: false, message: "Failed to resend OTP" };
    }
};





// ✅ Detects if the identifier is an email or phone number
// const isEmail = (identifier) => /\S+@\S+\.\S+/.test(identifier);

// ✅ Login API Call (Handles Email & Phone Login)
export const login = async (credentials) => {
    try {
        console.log("🟢 Login Function Received:", credentials);

        const requestData = {
            email: credentials.email,
            password: credentials.password
        };

        console.log("🟢 Login Request Data:", requestData);

        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData),
        });

        const data = await response.json();
        console.log("🔴 API Response:", data); // ✅ Debugging Response

        if (!response.ok) {
            return { success: false, message: data.detail || "Login failed" };
        }

      localStorage.setItem("token", data.token);
      localStorage.setItem("isLoggedIn", "true");  // ✅ Store login state
      window.dispatchEvent(new Event("storage"));
        return { success: true, message: data.message, access_token: data.access_token };
    } catch (error) {
        console.error("🔴 Login Request Failed:", error);
        return { success: false, message: "Server error. Please try again later." };
    }
};



// ✅ Logout Function
export const logout = () => {
    console.log("✅ Logout function called!");

    // ✅ Clear authentication data
    localStorage.removeItem("token");
    localStorage.removeItem("isLoggedIn");

    // ✅ Notify all components to update UI
    window.dispatchEvent(new Event("storage")); 

    // ✅ Redirect to Landing Page (`/`)
    window.location.href = "/";
};



// ✅ Check if user is authenticated
export const isAuthenticated = () => !!localStorage.getItem("token");
