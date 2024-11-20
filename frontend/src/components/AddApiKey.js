import React, { useState } from 'react';
import { addApiKey } from '../services/api';
import { toast } from 'react-toastify';

function AddApiKey() {
  const [api_key, setApiKey] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addApiKey({ api_key });
      toast.success('API Key added successfully');
    } catch (error) {
      toast.error('Failed to add API Key');
    }
  };

  return (
    <div className="form-container">
      <h2>Add API Key</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="API Key"
          value={api_key}
          onChange={(e) => setApiKey(e.target.value)}
          required
        />
        <button type="submit">Add API Key</button>
      </form>
    </div>
  );
}

export default AddApiKey;
