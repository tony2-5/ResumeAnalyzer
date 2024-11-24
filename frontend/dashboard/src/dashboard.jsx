import React, { useState, useEffect } from "react";
import "./dashboard.css";
import { mockData } from "./mock-data";

const Dashboard = () => {
  const [fitScore, setFitScore] = useState(null);
  const [skillsMatched, setSkillsMatched] = useState([]);
  const [improvementSuggestions, setImprovementSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Mock API request
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Simulate API call with a delay
        await new Promise((resolve) => setTimeout(resolve, 2000));
        // Simulate API call failure with a delay
        // await new Promise((_, reject) => setTimeout(() => reject(new Error("Simulated API failure")), 2000));
        setFitScore(mockData.fitScore);
        setSkillsMatched(mockData.skillsMatched);
        setImprovementSuggestions(mockData.improvementSuggestions);
      } catch (err) {
        setError("Failed to fetch data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

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
            ></div>
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
  );
};

export default Dashboard;
