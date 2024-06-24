const axios = require('axios');

const BASE_URL = 'http://localhost:8080';

// Function to fetch roadmaps from the server
exports.fetchDashboard = async function fetchDashboard() {
    try {
        const response = await axios.get(`${BASE_URL}/dashboard`);
        return response.data;
    } catch (error) {
        throw new Error('Failed to fetch roadmaps');
    }
}

// Function to fetch a specific roadmap by ID
exports.fetchRoadmap = async function fetchRoadmap(roadmapId) {
    try {
        const response = await axios.get(`${BASE_URL}/roadmap/${roadmapId}`);
        return response.data;
    } catch (error) {
        throw new Error(`Failed to fetch roadmap with ID: ${roadmapId}`);
    }
}

// Function to create a new roadmap
exports.createRoadmap = async function createRoadmap(roadmapData) {
    try {
        const response = await axios.post(`${BASE_URL}/create_roadmap`, roadmapData, {
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return response.data;
    } catch (error) {
        throw new Error('Failed to create roadmap');
    }
}

// Function to update the status of a roadmap
exports.updateRoadmapStatus = async function updateRoadmapStatus(roadmapId, newStatus) {
    try {
        const response = await axios.put(`${BASE_URL}/update_roadmap_status/${roadmapId}`, { new_status: newStatus }, {
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return response.data;
    } catch (error) {
        throw new Error(`Failed to update status for roadmap with ID: ${roadmapId}`);
    }
}
