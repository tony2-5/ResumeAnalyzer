import React, { useState, useEffect } from "react";
import "../dashboard.css";
import { useNavigate } from "react-router-dom";
import axiosInstance from '../api/axios';
import ResumeDescriptionUpload from "./ResumeDescriptionUpload";
import jsPDF from 'jspdf';

const Dashboard = () => {
    const [fitScore, setFitScore] = useState(null);
    const [matchedKeywords, setMatchedKeywords] = useState([]);
    const [feedback, setFeedback] = useState([]);
    const [data, setDataFromChild] = useState(null);
    const [filter, setFilter] = useState("all");
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
                localStorage.clear()
                navigate('/login');
            }
        };
        fetchUserData();
    }, [navigate]);

    // Fetch Fit Score Data
    useEffect(() => {
        if (data && data.resumeText!=null && data.jobDescription!=null) {
            console.log(data)
            setLoading(true);
            const fetchFitScoreData = async () => {
                try {
                    const response = await axiosInstance.post('/api/fit-score', {
                        resumeText: data.resumeText,
                        jobDescription: data.jobDescription
                    }, {
                        headers: {
                            'session-token': localStorage.getItem('accessToken')
                        }
                    });
                    const fitScoreData = response.data;
                    setFitScore(fitScoreData.fitScore);
                    setMatchedKeywords(fitScoreData.matchedKeywords)
                    setFeedback(fitScoreData.feedback.suggestions);
                } catch (err) {
                    setError("Failed to fetch fit score data. Please try again.");
                } finally {
                    setLoading(false);
                }
            };
            fetchFitScoreData();
        }
    }, [data]);

    const generatePDF = () => {
        const doc = new jsPDF();
        doc.setFont("helvetica", "bold");
        // Title
        doc.text("Resume Analysis Report", 10, 10);
    
        // Fit Score
        doc.text(`Fit Score: ${fitScore}%`, 10, 20);
    
        // Matched Keywords
        doc.text("Matched Keywords:", 10, 30);
        doc.setFont("helvetica", "normal");
        let yPosition = 40; // Initial position for matched keywords
        matchedKeywords.forEach((keyword, index) => {
            const wrappedText = doc.splitTextToSize(`- ${keyword}`, 180); // Wrap the keyword text
            wrappedText.forEach(line => {
                doc.text(line, 10, yPosition);
                yPosition += 10; // Increment yPosition for each line
            });
        });
        
        // Feedback
        doc.setFont("helvetica", "bold");
        doc.text("Feedback:", 10, yPosition + 10); // Add extra space before feedback
        doc.setFont("helvetica", "normal");
        yPosition += 20; // Adjust position for feedback section
        feedback.forEach((item, index) => {
            const wrappedText = doc.splitTextToSize(`- ${item.text}`, 180); // Wrap feedback text
            wrappedText.forEach(line => {
                doc.text(line, 10, yPosition);
                yPosition += 10; // Increment yPosition for each line of wrapped text
            });
        });
    
        // Save PDF
        doc.save("Resume_Analysis_Report.pdf");
    };

    // Filter Feedback
    const filteredFeedback = feedback.filter((item) =>
        filter === "all" ? true : item.category === filter
    );

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

                {/* Fit Score Section */}
                <div className="section">
                    <h2>Resume Fit Score</h2>
                    <div className="fit-score">
                        <div className="progress-bar">
                            <div
                                className="progress"
                                style={{ width: `${fitScore}%` }}
                            ></div>
                        </div>
                        <p>{fitScore}% Match</p>
                    </div>
                </div>

                {/* Matched Skills Section */}
                <div className="section">
                    <h2>Skills and Keywords Matched</h2>
                    <ul>
                        {matchedKeywords.map((skill, index) => (
                            <li key={index}>{skill}</li>
                        ))}
                    </ul>
                </div>

                {/* Improvement Suggestions Section */}
                <div className="section">
                    <h2>Improvement Suggestions</h2>
                    <select onChange={(e) => setFilter(e.target.value)}>
                        <option value="all">All</option>
                        <option value="skills">Skills</option>
                        <option value="experience">Experience</option>
                        <option value="education">Education</option>
                        <option value="achievements">Achievements</option>
                    </select>
                    <ul>
                        {filteredFeedback.map((suggestion, index) => (
                            <li key={index}>{suggestion.text}</li>
                        ))}
                    </ul>
                </div>

                {/* Download PDF Button */}
                <div className="section">
                    <button onClick={generatePDF}>Download PDF Report</button>
                </div>
            </div>
        </>
    );
};

export default Dashboard;
