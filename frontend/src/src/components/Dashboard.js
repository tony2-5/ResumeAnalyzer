import React, { useState, useEffect } from "react";
import "../dashboard.css";
import { mockData } from "../mock_data";
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
                const response = await axiosInstance.get('/api/users/me');
            } catch (error) {
                // Redirect to login page on error
                navigate('/login');
            }
        };
        fetchUserData();
    }, [navigate]);

    // Mock API request
    useEffect(() => {
        if (data) {
            setLoading(true);
            // Use an async function within the useEffect
            const fetchData = async () => {
                try {
                    await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulate delay
                    setFitScore(mockData.fitScore);
                    setSkillsMatched(mockData.skillsMatched);
                    setImprovementSuggestions(mockData.improvementSuggestions);
                    // data from form submission
                    console.log(data);
                } catch (err) {
                    setError("Failed to fetch data. Please try again.");
                } finally {
                    setLoading(false);
                }
            };
            fetchData()
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
            <button onClick={()=>{
                localStorage.clear(); 
                window.location.reload()}}>
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
                            <div
                            className="progress"
                            style={{ width: `${fitScore}%` }}
                            >
                            </div>
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
