import axios from 'axios';

// Create an Axios instance
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000', // Replace with the Backend URL Later
});

// Set up request interceptors to include JWT token and session-token
axiosInstance.interceptors.request.use(
    (config) => {
        const accessToken = localStorage.getItem('accessToken');

        if (accessToken) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default axiosInstance;
