// frontend/src/App.js
import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import ResumeUpload from './components/ResumeUpload';
import SignUpForm from './components/SignUpForm';

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

      {/* Always render the ResumeUpload form */}
      <ResumeUpload />
    </div>
  );
}

export default App;
