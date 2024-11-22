// src/components/Login.js

import React, { useState } from 'react';
import axios from '../api/axios';
import { useHistory } from 'react-router-dom';

function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [errorMessage, setErrorMessage] = useState('');
    const history = useHistory();

    const { email, password } = formData;

    // Handles input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({ ...prevState, [name]: value }));
    };

    // Handles form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('/api/login', {
                email,
                password,
            });
            // Store token in localStorage
            localStorage.setItem('accessToken', response.data.accessToken);
            // Redirect to dashboard
            history.push('/dashboard');
        } catch (error) {
            if (error.response && error.response.data.detail) {
                setErrorMessage(error.response.data.detail);
            } else {
                setErrorMessage('An error occurred. Please try again.');
            }
        }
    };

    return (
        <div className="login-form">
            <h2>Login</h2>
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
                {/* Error Message */}
                {errorMessage && <p className="error">{errorMessage}</p>}
                {/* Submit Button */}
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;
