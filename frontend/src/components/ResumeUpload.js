// frontend/src/components/ResumeUpload.js
import React, { useState } from 'react';

const ResumeUpload = () => {
    const [resumeFile, setResumeFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [message, setMessage] = useState('');

    // Handle resume file selection
    const handleResumeChange = (e) => {
        setResumeFile(e.target.files[0]);
    };

    // Handle job description input
    const handleJobDescriptionChange = (e) => {
        setJobDescription(e.target.value);
    };

    // Handle resume file upload
    const handleResumeSubmit = async () => {
        if (!resumeFile) {
            setMessage('Please select a resume file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', resumeFile);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/resume/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to upload resume.');
            }

            setMessage('Resume uploaded successfully.');
        } catch (error) {
            setMessage(error.message);
        }
    };

    // Handle job description upload
    const handleJobDescriptionSubmit = async () => {
        if (!jobDescription) {
            setMessage('Please enter a job description.');
            return;
        }

        const formData = new FormData();
        formData.append('job_desc', jobDescription);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/job-description/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to upload job description.');
            }

            setMessage('Job description uploaded successfully.');
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div>
            <h2>Upload Resume</h2>
            <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleResumeChange}
            />
            <button onClick={handleResumeSubmit}>Upload Resume</button>

            <h2>Upload Job Description</h2>
            <textarea
                placeholder="Enter job description"
                value={jobDescription}
                onChange={handleJobDescriptionChange}
            />
            <button onClick={handleJobDescriptionSubmit}>Upload Job Description</button>

            <p>{message}</p>
        </div>
    );
};

export default ResumeUpload;
