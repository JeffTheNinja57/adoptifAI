import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getAnimal } from '../services/api';
import { isAuthenticated } from '../utils/auth';
import { Link } from 'react-router-dom';

function AnimalDetail() {
  const { id } = useParams();
  const [animal, setAnimal] = useState(null);

  useEffect(() => {
    async function fetchAnimal() {
      try {
        const data = await getAnimal(id);
        setAnimal(data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchAnimal();
  }, [id]);

  if (!animal) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>{animal.name}</h2>
      <p>Type: {animal.animal_type}</p>
      <p>Age: {animal.age}</p>
      <p>Color: {animal.color}</p>
      <p>Behavior: {animal.behavior}</p>
      <p>Health: {animal.health}</p>
      <p>Vaccinated: {animal.vaccinated ? 'Yes' : 'No'}</p>
      <p>Target Audience: {animal.target_audience}</p>
      <p>Description: {animal.description_en}</p>
      {isAuthenticated() && (
        <>
          <Link to={`/update-animal/${animal.id}`}>Update Animal</Link>
          <Link to={`/generate-description/${animal.id}`}>Generate Description</Link>
        </>
      )}
    </div>
  );
}

export default AnimalDetail;
