import React, {useEffect, useState} from 'react';
import {getMyAnimals} from '../services/api';
import {Link} from 'react-router-dom';
import {toast} from 'react-toastify';

function MyAnimals() {
    const [animals, setAnimals] = useState([]);

    useEffect(() => {
        async function fetchMyAnimals() {
            try {
                const data = await getMyAnimals();
                setAnimals(data);
            } catch (error) {
                toast.error('Failed to load your animals');
            }
        }

        fetchMyAnimals();
    }, []);

    return (
        <div>
            <h2>My Animals</h2>
            <ul className="animal-list">
                {animals.map((animal) => (
                    <li key={animal.id}>
                        <Link to={`/animals/${animal.id}`}>{animal.name} - {animal.animal_type}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default MyAnimals;
