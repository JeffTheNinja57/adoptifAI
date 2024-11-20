import React, { useState } from 'react';

const NoApiKey = ({ onAddApiKey, onContinueWithoutApiKey }) => {
    const [apiKey, setApiKey] = useState('');

    const handleAddApiKey = () => {
        if (apiKey) {
            localStorage.setItem('apiKey', apiKey);
            onAddApiKey(apiKey);
        }
    };

    return (
        <div>
            <h2>You don't have an API key, you won't be able to generate descriptions.</h2>
            <input
                type="text"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter API Key"
            />
            <button onClick={handleAddApiKey}>Add API Key</button>
            <button onClick={onContinueWithoutApiKey}>I'm ok with that / Continue without an API key</button>
        </div>
    );
};

export default NoApiKey;