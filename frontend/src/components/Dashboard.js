// src/components/Dashboard.js

import React, { useEffect, useState } from 'react';
import axios from '../api/axios';
import { useHistory } from 'react-router-dom';

function Dashboard() {
    const [userData, setUserData] = useState(null);
    const history = useHistory();

    // Fetches user data on component mount
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await axios.get('/api/users/me');
                setUserData(response.data);
            } catch (error) {
                // Redirect to login page on error
                history.push('/login');
            }
        };
        fetchUserData();
    }, [history]);

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
