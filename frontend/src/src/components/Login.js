import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axiosInstance from '../api/axios';
import "../register-login.css";

const Login = () => {
		const [formData, setFormData] = useState({ email: "", password: "" });
		const [errorMessage, setErrorMessage] = useState('');

		const handleChange = (e) => {
				setFormData({ ...formData, [e.target.name]: e.target.value });
		};

		const handleSubmit = async (e) => {
				e.preventDefault();

				if (!/\S+@\S+\.\S+/.test(formData.email)) {
					setErrorMessage('Invalid email address.');
					return;
				}
				
				try {
						const response = await axiosInstance.post('/api/login',{
								email: formData.email,
								password: formData.password
						});
						// Store token in localStorage
						localStorage.setItem('accessToken', response.data.accessToken);
						// reload page to navigate to dashboard
						window.location.reload()
				} catch (error) {
						if (error.response && error.response.data.detail) {
							setErrorMessage(error.response.data.detail);
						} else {
							setErrorMessage('An error occurred. Please try again.');
						}
				}
		};

		return (
				<div>
						<h1>Login</h1>
						<form onSubmit={handleSubmit}>
								<div>
										<label htmlFor="email">Email: </label>
										<input
											type="email"
											id="email"
											name="email"
											value={formData.email}
											onChange={handleChange}
											required
										/>
								</div>
								<div>
										<label htmlFor="password">Password: </label>
										<input
											type="password"
											id="password"
											name="password"
											value={formData.password}
											onChange={handleChange}
											required
										/>
								</div>
								{errorMessage && <p className="error">{errorMessage}</p>}
								<button type="submit">Login</button>
								<p>Don’t have an account? <Link to="/register">Register here</Link>.</p>
						</form>
				</div>
		);
};

export default Login;
