// frontend/src/App.js
import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import SignUpForm from './components/SignUpForm';
import ResumeUpload from './components/ResumeUpload';

function App() {
  const [isSignUp, setIsSignUp] = useState(false);  // Track whether to show the SignUp form

  return (
    <div>
      <h1>Resume Analyzer</h1>

      {/* Conditionally render SignUp or Login form */}
      {isSignUp ? (
        <SignUpForm />
      ) : (
        <LoginForm />
      )}

      {/* Single button that toggles between Login and SignUp */}
      <button onClick={() => setIsSignUp(!isSignUp)}>
        {isSignUp ? "Already have an account? Log in" : "Don't have an account? Sign Up"}
      </button>

      {/* Only render the ResumeUpload form */}
      <ResumeUpload />
    </div>
  );
}

export default App;
