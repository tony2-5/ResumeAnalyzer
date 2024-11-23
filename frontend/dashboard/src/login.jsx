import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./auth-context";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = () => {
    login(); // Set authentication status
    navigate("/dashboard"); // Navigate to dashboard
  };

  return (
    <div>
      <h1>Login Page</h1>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Login;
