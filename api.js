/**
 * API service for communicating with the FastAPI backend.
 * Handles all HTTP requests with authentication.
 */

import axios from 'axios';
import { auth } from '../config/firebase';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  async (config) => {
    const user = auth.currentUser;
    if (user) {
      const token = await user.getIdToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication
export const authAPI = {
  verifyToken: (token) => api.post('/api/auth/verify', { token }),
  getCurrentUser: () => api.get('/api/auth/me'),
};

// Analysis
export const analysisAPI = {
  analyzeResume: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/analyze/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  analyzeText: (text) => {
    const formData = new FormData();
    formData.append('text', text);
    return api.post('/api/analyze/text', formData);
  },
  getSkillCategories: () => api.get('/api/analyze/skills/categories'),
};

// Career Prediction
export const predictionAPI = {
  predictCareers: (profile) => api.post('/api/predict/career', profile),
  listCareers: () => api.get('/api/predict/careers'),
  getCareerDetails: (careerTitle) => api.get(`/api/predict/career/${careerTitle}`),
  analyzeSkillGaps: (careerTitle, skills) =>
    api.post(`/api/predict/skill-gaps/${careerTitle}`, skills),
};

// Roadmap
export const roadmapAPI = {
  generateRoadmap: (careerPath, missingSkills, currentSkills) =>
    api.post('/api/roadmap/generate', {
      career_path: careerPath,
      missing_skills: missingSkills,
      current_skills: currentSkills,
    }),
  getRoadmap: (roadmapId) => api.get(`/api/roadmap/${roadmapId}`),
  getUserRoadmaps: () => api.get('/api/roadmap/user/roadmaps'),
  getSkillResources: (skill) => api.get(`/api/roadmap/resources/${skill}`),
  deleteRoadmap: (roadmapId) => api.delete(`/api/roadmap/${roadmapId}`),
};

// User Profile
export const userAPI = {
  saveProfile: (profile) => api.post('/api/user/profile', profile),
  getProfile: () => api.get('/api/user/profile'),
  getAnalyses: () => api.get('/api/user/analyses'),
  getAnalysis: (analysisId) => api.get(`/api/user/analysis/${analysisId}`),
  deleteProfile: () => api.delete('/api/user/profile'),
};

export default api;
