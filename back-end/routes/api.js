const express = require('express');
const router = express.Router();
const { fetchDashboard, fetchRoadmap, createRoadmap, updateRoadmapStatus } = require('../controllers/roadmapController');
const { registerUser, loginUser, logoutUser, getProfile, requestPasswordResetToken, updatePassword } = require('../controllers/userController')

router.use(express.json());

// Routes

// Roadmap routes
router.get('/dashboard', fetchDashboard);
router.get('/roadmap/:roadmapId', fetchRoadmap);
router.post('/newRoadmap', createRoadmap);
router.put('/updateRoadmap/:roadmapId', updateRoadmapStatus);

// User routes
router.post('/register', registerUser);
router.post('/login', loginUser);
router.delete('/logout', logoutUser);
router.get('/profile', getProfile);
router.post('/resetPassword', requestPasswordResetToken);
router.put('/resetPassword', updatePassword);

// TODO: Ai routes

module.exports = router;
