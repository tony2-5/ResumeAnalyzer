// src/components/Dashboard.js

import React, { useEffect, useState } from 'react';
import axiosInstance from '../api/axios';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
    const [userData, setUserData] = useState(null);
    const navigate = useNavigate();

    // Fetches user data on component mount
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await axiosInstance.get('/api/users/me');
                setUserData(response.data);
            } catch (error) {
                // Redirect to login page on error
                navigate('/login');
            }
        };
        fetchUserData();
    }, [navigate]);

    return (
        <div className="dashboard">
            <h2>Dashboard</h2>
            {userData ? (
                <p>Welcome, {userData.username}!</p>
            ) : (
                <p>Loading user data...</p>
            )}
        </div>
    );
}

export default Dashboard;
