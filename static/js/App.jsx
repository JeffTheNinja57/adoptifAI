// App.jsx
import React, { useState, useEffect } from 'react';
import AnimalListing from './components/AnimalListing';
import Login from './components/login';

const App = () => {
    const [token, setToken] = useState(null);

    useEffect(() => {
        const storedApiKey = localStorage.getItem('apiKey');
        if (storedApiKey) {
            setToken(storedApiKey);
        }
    }, []);

    if (!token) {
        return <Login onLogin={(token) => setToken(token)} />;
    }

    return (
        <div className="app-container">
            <h1>AdoptifAI - Find Your Perfect Pet</h1>
            <AnimalListing token={token} />
        </div>
    );
};

export default App;
