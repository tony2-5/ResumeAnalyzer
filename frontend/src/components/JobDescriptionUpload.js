// frontend/src/components/JobDescriptionUpload.js
import React, { useState } from 'react';

const JobDescriptionUpload = () => {
    const [jobDesc, setJobDesc] = useState('');
    const [message, setMessage] = useState('');

    const handleJobDescriptionUpload = async (e) => {
        e.preventDefault();

        if (!jobDesc) {
            setMessage("Please provide a job description.");
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/job-description', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ job_desc: jobDesc }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong');
            }

            setMessage('Job description uploaded successfully!');
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div>
            <form onSubmit={handleJobDescriptionUpload}>
                <textarea
                    placeholder="Enter job description"
                    value={jobDesc}
                    onChange={(e) => setJobDesc(e.target.value)}
                />
                <button type="submit">Upload Job Description</button>
            </form>
            <p>{message}</p>
        </div>
    );
};

export default JobDescriptionUpload;
