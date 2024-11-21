// src/components/AddAnimal.js

import React, { useState } from 'react';
import { addAnimal } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import {
  TextField,
  Button,
  Checkbox,
  FormControlLabel,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Paper,
  Typography,
} from '@mui/material';

function AddAnimal() {
  const [formData, setFormData] = useState({
    name: '',
    animal_type: 'dog',
    age: '',
    color: '',
    months_in_shelter: '',
    behavior: '',
    health: 'excellent',
    vaccinated: false,
    target_audience: '',
  });
  const [generateDesc, setGenerateDesc] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newAnimal = await addAnimal(formData);
      if (generateDesc) {
        // Optionally generate description here
      }
      toast.success('Animal added successfully');
      navigate('/account');
    } catch (error) {
      toast.error('Failed to add animal');
    }
  };

  return (
    <Paper className="form-container" style={{ padding: '2rem', marginTop: '2rem' }}>
      <Typography variant="h5" gutterBottom>
        Add New Animal
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <FormControl fullWidth margin="normal">
          <InputLabel>Animal Type</InputLabel>
          <Select
            value={formData.animal_type}
            onChange={(e) => setFormData({ ...formData, animal_type: e.target.value })}
            required
          >
            <MenuItem value="dog">Dog</MenuItem>
            <MenuItem value="cat">Cat</MenuItem>
          </Select>
        </FormControl>
        <TextField
          label="Age"
          type="number"
          value={formData.age}
          onChange={(e) => setFormData({ ...formData, age: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Color"
          value={formData.color}
          onChange={(e) => setFormData({ ...formData, color: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Months in Shelter"
          type="number"
          value={formData.months_in_shelter}
          onChange={(e) => setFormData({ ...formData, months_in_shelter: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Behavior"
          value={formData.behavior}
          onChange={(e) => setFormData({ ...formData, behavior: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <FormControl fullWidth margin="normal">
          <InputLabel>Health</InputLabel>
          <Select
            value={formData.health}
            onChange={(e) => setFormData({ ...formData, health: e.target.value })}
            required
          >
            <MenuItem value="excellent">Excellent</MenuItem>
            <MenuItem value="good">Good</MenuItem>
            <MenuItem value="bad">Bad</MenuItem>
          </Select>
        </FormControl>
        <FormControlLabel
          control={
            <Checkbox
              checked={formData.vaccinated}
              onChange={(e) => setFormData({ ...formData, vaccinated: e.target.checked })}
            />
          }
          label="Vaccinated"
        />
        <TextField
          label="Target Audience"
          value={formData.target_audience}
          onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
          required
          fullWidth
          margin="normal"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={generateDesc}
              onChange={(e) => setGenerateDesc(e.target.checked)}
            />
          }
          label="Generate Description"
        />
        <Button variant="contained" color="primary" type="submit" fullWidth style={{ marginTop: '1rem' }}>
          Add Animal
        </Button>
      </form>
    </Paper>
  );
}

export default AddAnimal;
