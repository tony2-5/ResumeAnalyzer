// frontend/src/components/SignUpForm.js
import React, { useState } from 'react';

const SignUpForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Check if any fields are empty
        if (!username || !password || !confirmPassword) {
            setMessage('All fields are required');
            return;
        }

        if (password !== confirmPassword) {
            setMessage("Passwords do not match!");
            return;
        }

        const credentials = { username, password };

        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(credentials),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong');
            }

            setMessage('Sign-up successful! Please log in.');
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button type="submit">Sign Up</button>
            </form>
            <p>{message}</p>
        </div>
    );
};

export default SignUpForm;
