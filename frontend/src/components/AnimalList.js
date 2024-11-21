// src/components/AnimalList.js

import React, { useEffect, useState } from 'react';
import { getAnimals } from '../services/api';
import { Link } from 'react-router-dom';
import { List, ListItem, ListItemText, Paper } from '@mui/material';

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
      <Paper>
        <List>
          {animals.map((animal) => (
            <ListItem button component={Link} to={`/animals/${animal.id}`} key={animal.id}>
              <ListItemText primary={`${animal.name} - ${animal.animal_type}`} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </div>
  );
}

export default AnimalList;
