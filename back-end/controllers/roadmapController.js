const axios = require('axios');

const BASE_URL = 'http://localhost:8080';

// Function to fetch roadmaps from the server
exports.fetchDashboard = async function fetchDashboard(_req, res) {
    try {
        const response = await axios.get(`${BASE_URL}/dashboard`);
        roadmaps = await response.data;
        res.json(roadmaps);
    } catch (error) {
        console.error(error);
        return res.status(500).json({"message": "Internal Server Error"})
    }
}

// Function to fetch a specific roadmap by ID
exports.fetchRoadmap = async function fetchRoadmap(req, res) {
    const { roadmapId } = req.params;
    try {
        const response = await axios.get(`${BASE_URL}/roadmap/${roadmapId}`);
        const roadmap = await response.data;
        res.json(roadmap);
    } catch (error) {
        // console.error(error);
        if (error.response && error.response.status === 404) {
            return res.status(404).json({"message": "Roadmap not found"})
        }
        return res.status(500).json({"message": "Internal Server Error"})
    }
}

// Function to create a new roadmap
exports.createRoadmap = async function createRoadmap(req, res) {
    const { user_id, Roadmap } = req.body;  // Corrected from req.form to req.body

    try {
        const response = await axios.post(`${BASE_URL}/create_roadmap`, {
            user_id: user_id,
            roadmaps: Roadmap  // Ensure roadmaps key is used
        }, {
            headers: {
                'Content-Type': 'application/json',
            }
        });

        return res.status(201).json(response.data);
    } catch (error) {
        // console.error(error);
        if (error.response && error.response.status === 400) {
            return res.status(400).json({"message": "User Not Found"})
        } else if (error.response && error.response.status === 403) {
            return res.status(403).json({"message": "Invalid Request Body"})
        }
        return res.status(500).json({"message": "Internal Server Error"})
    }
}

// Function to update the status of a roadmap
exports.updateRoadmapStatus = async function updateRoadmapStatus(req, res) {
    const { roadmapId } = req.params;
    const { newStatus } = req.body;
    try {
        const response = await axios.put(`${BASE_URL}/update_roadmap_status/${roadmapId}`, { new_status: newStatus }, {
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return res.status(200).json(response.data);
    } catch (error) {
        // console.error(error);
        if (error.response && error.response.status === 404) {
            return res.status(404).json({"message": "Roadmap not found"})
        } else if (error.response && error.response.status === 403) {
            return res.status(403).json({"message": "Invalid Request Body"})
        }
        return res.status(500).json({"message": "Internal Server Error"})
    }
}
