const express = require('express');
const router = express.Router();
const { fetchDashboard, fetchRoadmap, createRoadmap, updateRoadmapStatus } = require('../controllers/roadmapController');

router.use(express.json());

// Routes
router.get('/dashboard', async (_req, res, next) => {
    try {
        const roadmaps = await fetchDashboard();
        res.json(roadmaps);
    } catch (error) {
        next(error);
    }
});

router.get('/roadmap/:roadmapId', async (req, res, next) => {
    const { roadmapId } = req.params;
    try {
        const roadmap = await fetchRoadmap(roadmapId);
        res.json(roadmap);
    } catch (error) {
        next(error);
    }
});

router.post('/newRoadmap', async (req, res, next) => {
    const roadmapData = req.body;
    try {
        const createdRoadmap = await createRoadmap(roadmapData);
        res.json(createdRoadmap);
    } catch (error) {
        next(error);
    }
});

router.put('/updateRoadmap/:roadmapId', async (req, res, next) => {
    const { roadmapId } = req.params;
    const { newStatus } = req.body;
    try {
        const updatedRoadmap = await updateRoadmapStatus(roadmapId, newStatus);
        res.json(updatedRoadmap);
    } catch (error) {
        next(error);
    }
});

module.exports = router;
