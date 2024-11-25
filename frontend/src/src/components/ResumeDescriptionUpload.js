import React, { useState } from 'react';
import axiosInstance from '../api/axios'; // Import the custom Axios instance

const ResumeDescriptionUpload = ({setData}) => {
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
        formData.append('resume_file', resumeFile);

        try {
            await axiosInstance.post('/api/resume-upload', formData, {
                headers: { 
                    'Content-Type': 'multipart/form-data',
                    'session-token': localStorage.getItem('accessToken') 
                },
            });

            setMessage('Resume uploaded successfully.');
        } catch (error) {
            setMessage(error.response?.data?.detail || 'Failed to upload resume.');
        }
    };

    // Handle job description upload
    const handleJobDescriptionSubmit = async () => {
        if (!jobDescription) {
            setMessage('Please enter a job description.');
            return;
        }

        try {
            await axiosInstance.post('/api/job-description',
                {job_description: jobDescription},
                {
                headers: { 
                    'session-token': localStorage.getItem('accessToken') 
                }
            });

            setMessage('Job description uploaded successfully.');
        } catch (error) {
            setMessage(error.response?.data?.detail || 'Failed to upload job description.');
        }

        try {
            const response = await axiosInstance.get('/api/resume-data', {
                headers: {
                    'session-token': localStorage.getItem('accessToken')
                }
            });
            setData(response.data)
        } catch (error) {
            console.error('Error fetching resume data:');
        }
    };

    return (
        <div>
            <h2>Upload Resume</h2>
            <div className='resumeUpload'>
                <input
                    data-testid="resume"
                    type="file"
                    accept="application/pdf"
                    onChange={handleResumeChange}
                />
                <button onClick={handleResumeSubmit}>Upload Resume</button>
            </div>
            <h2>Upload Job Description</h2>
            <div className='resumeUpload'>
                <textarea
                    data-testid="description"
                    placeholder="Enter job description"
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                />
                <button onClick={handleJobDescriptionSubmit}>Upload Job Description</button>
            </div>
            <div className='message'>
                <p>{message}</p>
            </div>
        </div>
    );
};

export default ResumeDescriptionUpload;