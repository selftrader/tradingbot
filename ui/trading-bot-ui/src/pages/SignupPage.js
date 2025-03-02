import React, { useState } from "react";
import { signup } from "../services/authService";

const SignupPage = () => {
    const [form, setForm] = useState({ username: "", email: "", password: "" });
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    // ✅ Validate email format
    const isValidEmail = (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); // Regex for valid email
    };

    // ✅ Validate password strength
    const isValidPassword = (password) => {
        return password.length >= 8 && /\d/.test(password); // Must be 8+ characters & have a number
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setError(""); // Clear previous errors

        // Validate email format
        if (!isValidEmail(form.email)) {
            setError("Invalid email format. Please enter a valid email.");
            return;
        }

        // Validate password strength
        if (!isValidPassword(form.password)) {
            setError("Password must be at least 8 characters long and contain at least one number.");
            return;
        }

        const response = await signup(form);
        if (response.success) {
            setMessage("Signup successful. Please log in.");
        } else {
            setError(response.error);
        }
    };

    return (
        <div>
            <h2>Sign Up</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {message && <p style={{ color: "green" }}>{message}</p>}
            <form onSubmit={handleSignup}>
                <input type="text" placeholder="Username" required onChange={(e) => setForm({ ...form, username: e.target.value })} />
                <input type="email" placeholder="Email" required onChange={(e) => setForm({ ...form, email: e.target.value })} />
                <input type="password" placeholder="Password" required onChange={(e) => setForm({ ...form, password: e.target.value })} />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
};

export default SignupPage;
