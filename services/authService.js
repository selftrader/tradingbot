const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { User } = require('../models/user');
const { ACCESS_TOKEN_EXPIRE_MINUTES } = require('../config');

function authenticateUser(userData) {
    const user = User.findOne({ email: userData.email });
    if (!user || !bcrypt.compareSync(userData.password, user.password)) {
        throw new Error('Invalid credentials');
    }
    const accessToken = createAccessToken(user.username);
    const refreshToken = createRefreshToken(user.username);  // ✅ Define refreshToken
    return { accessToken, refreshToken, tokenType: "bearer" };
}

function createAccessToken(username) {
    const expire = new Date();
    expire.setMinutes(expire.getMinutes() + ACCESS_TOKEN_EXPIRE_MINUTES);
    const payload = { sub: username, exp: Math.floor(expire.getTime() / 1000) };
    return jwt.sign(payload, process.env.JWT_SECRET || "your-access-secret-key", { algorithm: "HS256" });
}

function createRefreshToken(username) {
    const expire = new Date();
    expire.setDate(expire.getDate() + 7);  // Refresh token valid for 7 days
    const payload = { sub: username, exp: Math.floor(expire.getTime() / 1000) };
    return jwt.sign(payload, process.env.REFRESH_SECRET || "your-refresh-secret-key", { algorithm: "HS256" });
}

module.exports = {
    authenticateUser,
    createAccessToken,
    createRefreshToken
};