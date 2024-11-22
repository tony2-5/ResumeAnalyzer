// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import SignUp from './components/SignUp';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
    const isAuthenticated = !!localStorage.getItem('accessToken');

    return (
        <Router>
            <Routes>
                <Route path="/signup" element={<SignUp />} />
                <Route path="/login" element={<Login />} />
                <Route path="/dashboard" 
                element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} 
                />
                <Route path="/" element={<Navigate to="/login" />} />
                {/* 404 Page */}
                <Route path="*" element={<h2>Page Not Found</h2>} />
            </Routes>
        </Router>
    );
}

export default App;