// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import SignUp from './components/SignUp';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
    const isAuthenticated = !!localStorage.getItem('accessToken');

    return (
        <Router>
            <Switch>
                <Route path="/signup" component={SignUp} />
                <Route path="/login" component={Login} />
                <Route path="/dashboard">
                    {isAuthenticated ? <Dashboard /> : <Redirect to="/login" />}
                </Route>
                <Route exact path="/">
                    <Redirect to="/login" />
                </Route>
                {/* 404 Page */}
                <Route path="*">
                    <h2>Page Not Found</h2>
                </Route>
            </Switch>
        </Router>
    );
}

export default App;
