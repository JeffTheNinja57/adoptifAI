import React, { useState } from 'react';

const Register = ({ onRegister }) => {
    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [contactEmail, setContactEmail] = useState('');
    const [apiKey, setApiKey] = useState('');

    const handleRegister = async () => {
        if (!apiKey) {
            alert("Please note: You need to obtain a Gemini API key to use all features. Visit the Gemini API provider's website to get your key.");
            return;
        }
        try {
            const response = await fetch('/api/shelter/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, location, contact_email: contactEmail, api_key: apiKey }),
            });
            const data = await response.json();
            if (response.ok) {
                alert(`Registration successful! Your API key: ${data.api_key}. Please save it.`);
                onRegister();
            } else {
                alert(`Registration failed: ${data.detail}`);
            }
        } catch (err) {
            console.error('Failed to register:', err);
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Shelter Name"
            />
            <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Location"
            />
            <input
                type="email"
                value={contactEmail}
                onChange={(e) => setContactEmail(e.target.value)}
                placeholder="Contact Email"
            />
            <input
                type="text"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Gemini API Key"
            />
            <button onClick={handleRegister}>Register</button>
        </div>
    );
};

export default Register;
