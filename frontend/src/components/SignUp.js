// src/components/SignUp.js

import React, { useState } from 'react';
import axios from '../api/axios';
import { useHistory } from 'react-router-dom';

function SignUp() {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        confirmPassword: '',
    });
    const [errorMessage, setErrorMessage] = useState('');
    const history = useHistory();

    const { email, username, password, confirmPassword } = formData;

    // Handles input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({ ...prevState, [name]: value }));
    };

    // Handles form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Check if passwords match
        if (password !== confirmPassword) {
            setErrorMessage('Passwords do not match.');
            return;
        }

        try {
            await axios.post('/api/register', {
                email,
                username,
                password,
            });
            // Redirect to login page upon successful registration
            history.push('/login');
        } catch (error) {
            if (error.response && error.response.data.detail) {
                setErrorMessage(error.response.data.detail);
            } else {
                setErrorMessage('An error occurred. Please try again.');
            }
        }
    };

    return (
        <div className="signup-form">
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit}>
                {/* Email Input */}
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={email}
                        onChange={handleChange}
                        required
                    />
                </div>
                {/* Username Input */}
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        name="username"
                        value={username}
                        onChange={handleChange}
                        required
                    />
                </div>
                {/* Password Input */}
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        name="password"
                        value={password}
                        onChange={handleChange}
                        required
                    />
                </div>
                {/* Confirm Password Input */}
                <div>
                    <label>Confirm Password:</label>
                    <input
                        type="password"
                        name="confirmPassword"
                        value={confirmPassword}
                        onChange={handleChange}
                        required
                    />
                </div>
                {/* Error Message */}
                {errorMessage && <p className="error">{errorMessage}</p>}
                {/* Submit Button */}
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default SignUp;
