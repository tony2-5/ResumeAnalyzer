import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axiosInstance from '../api/axios';
import "../register-login.css";

const Register = () => {
		const [formData, setFormData] = useState({
				email: '',
				username: '',
				password: '',
				confirmPassword: '',
		});
		const navigate = useNavigate();
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

			if (formData.password !== formData.confirmPassword) {
					setErrorMessage('Passwords do not match.');
					return;
			}

			try {
					await axiosInstance.post('/api/register', 
							{
									email: formData.email,
									username: formData.username,
									password: formData.password,
							}
					);
					// Redirect to login page upon successful registration
					navigate('/login');
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
					<h1>Register</h1>
					<form onSubmit={handleSubmit}>
							<div>
									<label htmlFor="registerEmail">Email: </label>
									<input
									id="registerEmail"
									type="email"
									name="email"
									value={formData.email}
									onChange={handleChange}
									required
									/>
							</div>
							<div>
									<label htmlFor="username">Username: </label>
									<input
										id="username"
										type="text"
										name="username"
										value={formData.username}
										onChange={handleChange}
										required
									/>
							</div>
							<div>
									<label htmlFor="registerPassword">Password: </label>
									<input
										id="registerPassword"
										data-testid="registerPassword"
										type="password"
										name="password"
										value={formData.password}
										onChange={handleChange}
										required
									/>
							</div>
							<div>
									<label htmlFor="confirmPassword">Confirm Password: </label>
									<input
									id="confirmPassword"
									data-testid="confirmPassword"
									type="password"
									name="confirmPassword"
									value={formData.confirmPassword}
									onChange={handleChange}
									required
									/>
							</div>
							{errorMessage && <p className="error">{errorMessage}</p>}
							<button type="submit">Register</button>
							<p>Already have an account? <Link to="/login">Login here</Link>.</p>
					</form>
				</div>
  	);
};

export default Register;
