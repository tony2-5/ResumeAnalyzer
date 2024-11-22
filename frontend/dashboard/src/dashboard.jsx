import React from "react";
import "./dashboard.css";

const Dashboard = ({ fitScore, skillsMatched, improvementSuggestions }) => {
  return (
    <div className="dashboard">
      <h1>Resume Analysis Results</h1>

      {/* Fit Score */}
      <div className="section">
        <h2>Resume Fit Score</h2>
        <div className="fit-score">
        <div className="progress-bar">
          <div className="progress" style={{ width: `${fitScore}%`}}></div>
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