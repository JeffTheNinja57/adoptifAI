// src/components/UpdateAnimal.js

import React, {useEffect, useState} from 'react';
import {getAnimal, updateAnimal} from '../services/api';
import {useNavigate, useParams} from 'react-router-dom';
import {toast} from 'react-toastify';
import {
    Button,
    Checkbox,
    FormControl,
    FormControlLabel,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    TextField,
    Typography,
} from '@mui/material';

function UpdateAnimal() {
    const {id} = useParams();
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
    const navigate = useNavigate();

    useEffect(() => {
        async function fetchAnimal() {
            try {
                const data = await getAnimal(id);
                setFormData({
                    name: data.name,
                    animal_type: data.animal_type,
                    age: data.age,
                    color: data.color,
                    months_in_shelter: data.months_in_shelter,
                    behavior: data.behavior,
                    health: data.health,
                    vaccinated: data.vaccinated,
                    target_audience: data.target_audience,
                });
            } catch (error) {
                toast.error('Failed to load animal data');
            }
        }

        fetchAnimal();
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await updateAnimal(id, formData);
            toast.success('Animal updated successfully');
            navigate('/account');
        } catch (error) {
            toast.error('Failed to update animal');
        }
    };

    return (
        <Paper className="form-container" style={{padding: '2rem', marginTop: '2rem'}}>
            <Typography variant="h5" gutterBottom>
                Update Animal
            </Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Name"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    required
                    fullWidth
                    margin="normal"
                />
                <FormControl fullWidth margin="normal">
                    <InputLabel>Animal Type</InputLabel>
                    <Select
                        value={formData.animal_type}
                        onChange={(e) => setFormData({...formData, animal_type: e.target.value})}
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
                    onChange={(e) => setFormData({...formData, age: e.target.value})}
                    required
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Color"
                    value={formData.color}
                    onChange={(e) => setFormData({...formData, color: e.target.value})}
                    required
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Months in Shelter"
                    type="number"
                    value={formData.months_in_shelter}
                    onChange={(e) => setFormData({...formData, months_in_shelter: e.target.value})}
                    required
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Behavior"
                    value={formData.behavior}
                    onChange={(e) => setFormData({...formData, behavior: e.target.value})}
                    required
                    fullWidth
                    margin="normal"
                />
                <FormControl fullWidth margin="normal">
                    <InputLabel>Health</InputLabel>
                    <Select
                        value={formData.health}
                        onChange={(e) => setFormData({...formData, health: e.target.value})}
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
                            onChange={(e) => setFormData({...formData, vaccinated: e.target.checked})}
                        />
                    }
                    label="Vaccinated"
                />
                <TextField
                    label="Target Audience"
                    value={formData.target_audience}
                    onChange={(e) => setFormData({...formData, target_audience: e.target.value})}
                    required
                    fullWidth
                    margin="normal"
                />
                <Button variant="contained" color="primary" type="submit" fullWidth style={{marginTop: '1rem'}}>
                    Update Animal
                </Button>
            </form>
        </Paper>
    );
}

export default UpdateAnimal;
