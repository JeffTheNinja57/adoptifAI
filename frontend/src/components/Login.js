import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import { saveToken } from '../utils/auth';
import { toast } from 'react-toastify';

function Login() {
  const [contact_email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await login({ username: contact_email, password });
      saveToken(response.access_token);
      toast.success('Login successful');
      navigate('/add-api-key');
    } catch (error) {
      toast.error('Invalid credentials');
    }
  };

  return (
    <div className="form-container">
      <h2>Shelter Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={contact_email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
