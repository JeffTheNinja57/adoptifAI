// src/components/AccountPage.js

import React, {useEffect, useState} from 'react';
import {
    deleteAnimal,
    deleteShelter,
    generateDescription,
    getMyAnimals,
    getShelterDetails,
    updateShelter,
    generateTranslation
} from '../services/api';
import {useNavigate} from 'react-router-dom';
import {isAuthenticated, logout} from '../utils/auth';
import {toast} from 'react-toastify';
import {Button, Paper, Table, TableBody, TableCell, TableHead, TableRow, TextField, Typography,} from '@mui/material';
import GenerateDescription from "./GenerateDescription";
import GenerateTranslation from "./GenerateTranslation";

function AccountPage() {
    const [shelter, setShelter] = useState(null);
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({});
    const [animals, setAnimals] = useState([]);
    const [selectedAnimal, setSelectedAnimal] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated()) {
            navigate('/login');
        } else {
            fetchShelterDetails();
            fetchMyAnimals();
        }
    }, []);

    const fetchShelterDetails = async () => {
        try {
            const data = await getShelterDetails();
            setShelter(data);
            setFormData({
                name: data.name,
                location: data.location,
                contact_email: data.contact_email,
                api_key: data.api_key || '',
            });
        } catch (error) {
            toast.error('Failed to load shelter details');
        }
    };

    const fetchMyAnimals = async () => {
        try {
            const data = await getMyAnimals();
            setAnimals(data);
        } catch (error) {
            toast.error('Failed to load animals');
        }
    };

    const handleUpdateShelter = async () => {
        try {
            await updateShelter(formData);
            toast.success('Shelter updated successfully');
            setEditing(false);
            fetchShelterDetails();
        } catch (error) {
            toast.error('Failed to update shelter');
        }
    };

    const handleDeleteShelter = async () => {
        if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            try {
                await deleteShelter();
                toast.success('Shelter deleted successfully');
                logout();
                navigate('/');
            } catch (error) {
                toast.error('Failed to delete shelter');
            }
        }
    };

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    const handleAnimalSelect = (animal) => {
        setSelectedAnimal(animal);
    };

    const handleAnimalAction = (action) => {
        if (!selectedAnimal) {
            toast.error('Please select an animal');
            return;
        }
        switch (action) {
            case 'edit':
                navigate(`/update-animal/${selectedAnimal.id}`);
                break;
            case 'delete':
                handleDeleteAnimal(selectedAnimal.id);
                break;
            case 'generateDescription':
                handleGenerateDescription(selectedAnimal.id);
                break;
            case 'generateTranslation':
                handleGenerateTranslation(selectedAnimal.id);
                break;
            default:
                break;
        }
    };

    const handleDeleteAnimal = async (animalId) => {
        if (window.confirm('Are you sure you want to delete this animal?')) {
            try {
                await deleteAnimal(animalId);
                toast.success('Animal deleted successfully');
                fetchMyAnimals();
                setSelectedAnimal(null);
            } catch (error) {
                toast.error('Failed to delete animal');
            }
        }
    };

    const handleGenerateDescription = async (animalId) => {
        try {
            await GenerateDescription(animalId);
            toast.success('Description generated successfully');
            fetchMyAnimals();
        } catch (error) {
            toast.error('Failed to generate description');
        }
    };

    const handleUploadCSV = () => {
        navigate('/upload-csv');
    };

    return (
        <div className="account-page" style={{padding: '1rem'}}>
            <div style={{display: 'flex'}}>
                <div style={{width: '50%', paddingRight: '1rem'}}>
                    <Typography variant="h5">My Animals</Typography>
                    <Paper>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Name</TableCell>
                                    <TableCell>Type</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {animals.map((animal) => (
                                    <TableRow
                                        key={animal.id}
                                        hover
                                        selected={selectedAnimal && selectedAnimal.id === animal.id}
                                        onClick={() => handleAnimalSelect(animal)}
                                    >
                                        <TableCell>{animal.name}</TableCell>
                                        <TableCell>{animal.animal_type}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Paper>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => navigate('/add-animal')}
                        style={{marginTop: '1rem'}}
                    >
                        Add Animal
                    </Button>
                </div>
                <div style={{width: '50%', paddingLeft: '1rem'}}>
                    <Typography variant="h5">Shelter Details</Typography>
                    {editing ? (
                        <div>
                            <TextField
                                label="Name"
                                value={formData.name}
                                onChange={(e) => setFormData({...formData, name: e.target.value})}
                                fullWidth
                                margin="normal"
                            />
                            <TextField
                                label="Location"
                                value={formData.location}
                                onChange={(e) => setFormData({...formData, location: e.target.value})}
                                fullWidth
                                margin="normal"
                            />
                            <TextField
                                label="Email"
                                value={formData.contact_email}
                                onChange={(e) => setFormData({...formData, contact_email: e.target.value})}
                                fullWidth
                                margin="normal"
                            />
                            <TextField
                                label="API Key"
                                value={formData.api_key}
                                onChange={(e) => setFormData({...formData, api_key: e.target.value})}
                                fullWidth
                                margin="normal"
                            />
                            <Button variant="contained" color="primary" onClick={handleUpdateShelter}>
                                Save Changes
                            </Button>
                            <Button variant="text" onClick={() => setEditing(false)}>
                                Cancel
                            </Button>
                        </div>
                    ) : (
                        <div>
                            <p>
                                <strong>Name:</strong> {shelter?.name}
                            </p>
                            <p>
                                <strong>Location:</strong> {shelter?.location}
                            </p>
                            <p>
                                <strong>Email:</strong> {shelter?.contact_email}
                            </p>
                            <p>
                                <strong>API Key:</strong> {shelter?.api_key ? shelter.api_key : 'Not Set'}
                            </p>
                            <Button variant="contained" color="primary" onClick={() => setEditing(true)}>
                                Edit Shelter
                            </Button>
                        </div>
                    )}
                    <div style={{marginTop: '1rem'}}>
                        <Typography variant="h6">Animal Actions</Typography>
                        <Button variant="contained" color="primary" onClick={() => handleAnimalAction('edit')}>
                            Edit Animal
                        </Button>
                        <Button
                            variant="contained"
                            color="secondary"
                            onClick={() => handleAnimalAction('delete')}
                            style={{marginLeft: '1rem'}}
                        >
                            Delete Animal
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => handleAnimalAction('generateDescription')}
                            style={{marginLeft: '1rem'}}
                        >
                            Generate Description
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => handleAnimalAction('generateTranslation')}
                            style={{marginLeft: '1rem'}}
                        >
                            Generate Translation
                        </Button>
                        {/* Add other buttons like Generate Translation, Mark as Adopted */}
                    </div>
                    <Button variant="contained" color="primary" onClick={handleUploadCSV} style={{marginTop: '1rem'}}>
                        Upload Data (CSV)
                    </Button>
                    <Button variant="contained" color="secondary" onClick={handleDeleteShelter}
                            style={{marginTop: '1rem'}}>
                        Delete Shelter
                    </Button>
                    <Button variant="text" onClick={handleLogout} style={{marginTop: '1rem'}}>
                        Logout
                    </Button>
                </div>
            </div>
        </div>
    );
}

export default AccountPage;
