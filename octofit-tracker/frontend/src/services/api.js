import { API_BASE_URL } from '../constants';

/**
 * API service for OctoFit Tracker
 * This service provides methods to interact with the backend API
 */

// Generic fetch function with error handling
const fetchAPI = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// API methods for different endpoints
export const apiService = {
  // Users
  getUsers: () => fetchAPI('/users/'),
  getUserById: (id) => fetchAPI(`/users/${id}/`),
  
  // Teams
  getTeams: () => fetchAPI('/teams/'),
  getTeamById: (id) => fetchAPI(`/teams/${id}/`),
  
  // Activities
  getActivities: () => fetchAPI('/activities/'),
  getActivityById: (id) => fetchAPI(`/activities/${id}/`),
  
  // Leaderboard
  getLeaderboard: () => fetchAPI('/leaderboard/'),
  
  // Workouts
  getWorkouts: () => fetchAPI('/workouts/'),
  getUserWorkouts: (userId) => fetchAPI(`/user-workouts/?user=${userId}`),
  
  // API Info
  getAPIInfo: () => fetchAPI(''),
};

export default apiService;