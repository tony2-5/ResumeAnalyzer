import axios from 'axios';

// Create an Axios instance
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000', // Replace with the Backend URL Later
});

// Set up request interceptors to include JWT token and session-token
axiosInstance.interceptors.request.use(
    (config) => {
        const accessToken = localStorage.getItem('accessToken');
        const sessionToken = localStorage.getItem('sessionToken'); // Assume sessionToken is stored in localStorage

        if (accessToken) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }

        if (sessionToken) {
            config.headers['session-token'] = sessionToken;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

export default axiosInstance;
