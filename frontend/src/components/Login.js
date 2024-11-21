// src/components/Login.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import { saveToken } from '../utils/auth';
import { toast } from 'react-toastify';
import { TextField, Button, Paper, Typography } from '@mui/material';

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
      navigate('/account');
    } catch (error) {
      toast.error('Invalid credentials');
    }
  };

  return (
    <Paper className="form-container" style={{ padding: '2rem', marginTop: '2rem' }}>
      <Typography variant="h5" gutterBottom>
        Shelter Login
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Email"
          type="email"
          value={contact_email}
          onChange={(e) => setEmail(e.target.value)}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          fullWidth
          margin="normal"
        />
        <Button variant="contained" color="primary" type="submit" fullWidth style={{ marginTop: '1rem' }}>
          Login
        </Button>
      </form>
    </Paper>
  );
}

export default Login;
