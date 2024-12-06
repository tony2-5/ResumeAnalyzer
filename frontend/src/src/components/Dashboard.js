import React, { useState, useEffect } from "react";
import "../dashboard.css";
import { useNavigate } from "react-router-dom";
import axiosInstance from '../api/axios';
import ResumeDescriptionUpload from "./ResumeDescriptionUpload";

const Dashboard = () => {
    const [fitScore, setFitScore] = useState(null);
    const [skillsMatched, setSkillsMatched] = useState([]);
    const [improvementSuggestions, setImprovementSuggestions] = useState([]);
    const [data, setDataFromChild] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Fetches user data on component mount
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                await axiosInstance.get('/api/users/me');
            } catch (error) {
                // Redirect to login page on error
                navigate('/login');
            }
        };
        fetchUserData();
    }, [navigate]);

    // Triggered when data is received from ResumeDescriptionUpload
    useEffect(() => {
        if (data) {
            setLoading(true);
            // Call the backend API to trigger the analysis
            const analyzeResume = async () => {
                try {
                    const accessToken = localStorage.getItem('accessToken');
                    const sessionToken = localStorage.getItem('session_token');  // Check if session-token exists
            
                    console.log("Access Token:", accessToken);  // Debug log
                    console.log("Session Token:", sessionToken);  // Debug log
            
                    const response = await axiosInstance.post('/api/analyze', {}, {
                        headers: { 
                            'Authorization': `Bearer ${accessToken}`,
                            'session-token': sessionToken || ''  // Send session-token if it exists
                        }
                    });
            
                    console.log("Response from backend:", response); // Log the full response
            
                    if (response.status === 200) {
                        const resultData = response.data.data;  // Access analysis result from the response
                        setFitScore(resultData.fitScore || 0);
                        setSkillsMatched(resultData.skillsMatched || []);
                        setImprovementSuggestions(resultData.improvementSuggestions || []);
                    }
                } catch (err) {
                    console.log("Error analyzing resume:", err); // Log the error details
                    setError("Failed to analyze data. Please try again.");
                } finally {
                    setLoading(false);
                }
            };

            analyzeResume();
        }
    }, [data]);

    if (loading) {
        return (
            <div className="spinner-container">
                <div className="spinner"></div>
                <p>Loading...</p>
            </div>
        );
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <>
            <button onClick={() => {
                localStorage.clear();
                window.location.reload();
            }}>
                Sign Out
            </button>
            <ResumeDescriptionUpload setData={setDataFromChild}></ResumeDescriptionUpload>
            <div className="dashboard">
                <h1>Resume Analysis Results</h1>

                {/* Fit Score */}
                <div className="section">
                    <h2>Resume Fit Score</h2>
                    <div className="fit-score">
                        <div className="progress-bar">
                            <div className="progress" style={{ width: `${fitScore}%` }} />
                        </div>
                        <p>{fitScore}% Match</p>
                    </div>
                </div>

                {/* Skills and Keywords Matched */}
                <div className="section">
                    <h2>Skills and Keywords Matched</h2>
                    <ul>
                        {skillsMatched.map((skill, index) => (
                            <li key={index}>{skill}</li>
                        ))}
                    </ul>
                </div>

                {/* Improvement Suggestions */}
                <div className="section">
                    <h2>Improvement Suggestions</h2>
                    <ul>
                        {improvementSuggestions.map((suggestion, index) => (
                            <li key={index}>{suggestion}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </>
    );
};

export default Dashboard;
