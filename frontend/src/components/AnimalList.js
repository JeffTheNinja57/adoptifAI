import React, { useEffect, useState } from 'react';
import { getAnimals } from '../services/api';
import { Link } from 'react-router-dom';

function AnimalList() {
  const [animals, setAnimals] = useState([]);

  useEffect(() => {
    async function fetchAnimals() {
      try {
        const data = await getAnimals();
        setAnimals(data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchAnimals();
  }, []);

  return (
    <div>
      <h2>Available Animals</h2>
      <ul className="animal-list">
        {animals.map((animal) => (
          <li key={animal.id}>
            <Link to={`/animals/${animal.id}`}>
              {animal.name} - {animal.animal_type}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AnimalList;
