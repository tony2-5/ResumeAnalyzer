// frontend/src/components/ResumeUpload.js
import React, { useState } from "react";

const ResumeUpload = () => {
    const [file, setFile] = useState(null);
    const [jobDesc, setJobDesc] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleJobDescChange = (e) => {
        setJobDesc(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", file);
        formData.append("job_desc", jobDesc);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/upload-resume/", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }

            const data = await response.json();
            console.log("Upload successful:", data);
        } catch (error) {
            console.error("Failed to upload:", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Upload Resume:
                <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} />
            </label>
            <br />
            <label>
                Job Description:
                <textarea value={jobDesc} onChange={handleJobDescChange} />
            </label>
            <br />
            <button type="submit">Submit</button>
        </form>
    );
};

export default ResumeUpload;
