// src/components/Register.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { register } from '../services/api';
import { toast } from 'react-toastify';
import { TextField, Button, Paper, Typography } from '@mui/material';

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    contact_email: '',
    password: '',
    api_key: '',
  });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(formData);
      toast.success('Registration successful');
      navigate('/login');
    } catch (error) {
      toast.error('Registration failed');
    }
  };

  return (
    <Paper className="form-container" style={{ padding: '2rem', marginTop: '2rem' }}>
      <Typography variant="h5" gutterBottom>
        Shelter Registration
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Shelter Name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Location"
          value={formData.location}
          onChange={(e) => setFormData({ ...formData, location: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Contact Email"
          type="email"
          value={formData.contact_email}
          onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="API Key (optional)"
          value={formData.api_key}
          onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
          fullWidth
          margin="normal"
        />
        <Button variant="contained" color="primary" type="submit" fullWidth style={{ marginTop: '1rem' }}>
          Register
        </Button>
      </form>
    </Paper>
  );
}

export default Register;
