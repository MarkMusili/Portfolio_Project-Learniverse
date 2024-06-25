const axios = require('axios');

const BASE_URL = 'http://localhost:8080';

exports.registerUser = async function registerUser(req, res) {
    const { firstName, lastName, email, password } = req.body;

    try {
        const response = await axios.post(`${BASE_URL}/users`, {
            first_name: firstName,
            last_name: lastName,
            email,
            password
        });

        res.status(201).json(response.data);
    } catch (error) {
        if (error.response && error.response.status === 400) {
            res.status(400).json({ message: "Email already registered" });
        } else {
            res.status(500).json({ message: "Internal server error" });
        }
    }
};

exports.loginUser = async function loginUser(req, res) {
    const { email, password } = req.body;

    try {
        const response = await axios.post(`${BASE_URL}/sessions`, {
            email,
            password
        });

        // Set session_id cookie
        res.cookie('session_id', response.data.session_id, { httpOnly: true });
        res.status(200).json(response.data);
    } catch (error) {
        if (error.response && error.response.status === 401) {
            res.status(401).json({ message: "Invalid credentials" });
        } else {
            res.status(500).json({ message: "Internal server error" });
        }
    }
};

exports.logoutUser = async function logoutUser(req, res) {
    const session_id = req.cookies.session_id;

    try {
        const response = await axios.delete(`${BASE_URL}/sessions`, {
            headers: { Cookie: `session_id=${session_id}` }
        });

        // Clear session_id cookie
        res.clearCookie('session_id');
        res.status(200).json(response.data);
    } catch (error) {
        if (error.response && error.response.status === 403) {
            res.status(403).json({ message: "Forbidden" });
        } else {
            res.status(500).json({ message: "Internal server error" });
        }
    }
};

exports.getProfile = async function getProfile(req, res) {
    const session_id = req.cookies.session_id;

    try {
        const response = await axios.get(`${BASE_URL}/profile`, {
            headers: { Cookie: `session_id=${session_id}` }
        });

        res.status(200).json(response.data);
    } catch (error) {
        if (error.response && error.response.status === 403) {
            res.status(403).json({ message: "Forbidden" });
        } else {
            res.status(500).json({ message: "Internal server error" });
        }
    }
};

exports.requestPasswordResetToken = async function requestPasswordResetToken(req, res) {
    const { email } = req.body;

    try {
        const response = await axios.post(`${BASE_URL}/reset_password`, { email });
        res.status(200).json(response.data);
    } catch (error) {
        if (error.response && error.response.status === 403) {
            res.status(403).json({ message: "Invalid email" });
        } else {
            res.status(500).json({ message: "Internal server error" });
        }
    }
};

exports.updatePassword = async function updatePassword(req, res) {
    const { email, reset_token, new_password } = req.body;

    try {
        const response = await axios.put(`${BASE_URL}/reset_password`, {
            email,
            reset_token,
            new_password
        });

        res.status(200).json(response.data);
    } catch (error) {
        if (error.response && error.response.status === 403) {
            res.status(403).json({ message: "Invalid token or email" });
        } else {
            res.status(500).json({ message: "Internal server error" });
        }
    }
};
