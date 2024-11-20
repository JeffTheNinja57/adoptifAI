// AnimalManagement.jsx
import React, { useState, useEffect } from 'react';
import animalService from '../services/animalService';

const AnimalManagement = ({ token }) => {
    const [animals, setAnimals] = useState([]);
    const [newAnimal, setNewAnimal] = useState({
        name: '',
        animal_type: '',
        age: '',
        color: '',
        months_in_shelter: 0,
        behavior: '',
        health: '',
        vaccinated: false,
        target_audience: ''
    });
    const [csvFile, setCsvFile] = useState(null);

    useEffect(() => {
        const loadAnimals = async () => {
            await fetchAnimals();
        };
        loadAnimals();
    }, []);

    const fetchAnimals = async () => {
        try {
            const data = await animalService.listAnimals(token); // Adding 'await'
            setAnimals(data);
        } catch (error) {
            console.error("Failed to load animals:", error);
        }
    };

    const handleAddAnimal = async () => {
        try {
            await animalService.addAnimal(newAnimal, token); // Adding 'await'
            alert('Animal added successfully');
            await fetchAnimals(); // Refresh the animal list after adding
        } catch (error) {
            console.error("Failed to add animal:", error);
        }
    };

    const handleDeleteAnimal = async (animalId) => {
        try {
            await animalService.deleteAnimal(animalId, token); // Adding 'await'
            alert('Animal deleted successfully');
            await fetchAnimals(); // Refresh the animal list after deletion
        } catch (error) {
            console.error("Failed to delete animal:", error);
        }
    };

    const handleImportCsv = async () => {
        if (!csvFile) {
            alert('Please upload a CSV file');
            return;
        }
        try {
            await animalService.importAnimals(csvFile, token); // Adding 'await'
            alert('Animals imported successfully');
            await fetchAnimals(); // Refresh the animal list after import
        } catch (error) {
            console.error('Failed to import animals:', error);
        }
    };

    return (
        <div>
            <h2>Manage Animals</h2>
            <div>
                <h3>Add New Animal</h3>
                <input
                    type="text"
                    value={newAnimal.name}
                    onChange={(e) => setNewAnimal({ ...newAnimal, name: e.target.value })}
                    placeholder="Name"
                />
                <input
                    type="text"
                    value={newAnimal.animal_type}
                    onChange={(e) => setNewAnimal({ ...newAnimal, animal_type: e.target.value })}
                    placeholder="Animal Type (e.g., dog, cat)"
                />
                <input
                    type="number"
                    value={newAnimal.age}
                    onChange={(e) => setNewAnimal({ ...newAnimal, age: parseFloat(e.target.value) })}
                    placeholder="Age"
                />
                <input
                    type="text"
                    value={newAnimal.color}
                    onChange={(e) => setNewAnimal({ ...newAnimal, color: e.target.value })}
                    placeholder="Color"
                />
                <input
                    type="number"
                    value={newAnimal.months_in_shelter}
                    onChange={(e) => setNewAnimal({ ...newAnimal, months_in_shelter: parseInt(e.target.value) })}
                    placeholder="Months in Shelter"
                />
                <input
                    type="text"
                    value={newAnimal.behavior}
                    onChange={(e) => setNewAnimal({ ...newAnimal, behavior: e.target.value })}
                    placeholder="Behavior"
                />
                <input
                    type="text"
                    value={newAnimal.health}
                    onChange={(e) => setNewAnimal({ ...newAnimal, health: e.target.value })}
                    placeholder="Health Status"
                />
                <input
                    type="checkbox"
                    checked={newAnimal.vaccinated}
                    onChange={(e) => setNewAnimal({ ...newAnimal, vaccinated: e.target.checked })}
                /> Vaccinated
                <input
                    type="text"
                    value={newAnimal.target_audience}
                    onChange={(e) => setNewAnimal({ ...newAnimal, target_audience: e.target.value })}
                    placeholder="Target Audience"
                />
                <button onClick={handleAddAnimal}>Add Animal</button>
            </div>
            <div>
                <h3>Import Animals from CSV</h3>
                <input type="file" onChange={(e) => setCsvFile(e.target.files[0])} />
                <button onClick={handleImportCsv}>Import Animals</button>
            </div>
            <div>
                <h3>Current Animals</h3>
                {animals.map((animal) => (
                    <div key={animal.id}>
                        <p>{animal.name} ({animal.animal_type})</p>
                        <button onClick={() => handleDeleteAnimal(animal.id)}>Delete</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AnimalManagement;
