// src/components/AnimalDetail.js

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getAnimal, generateDescription, generateTranslation } from '../services/api';
import { isAuthenticated } from '../utils/auth';
import { toast } from 'react-toastify';
import {
  Table,
  TableBody,
  TableCell,
  TableRow,
  Button,
  Typography,
  Paper,
} from '@mui/material';

function AnimalDetail() {
  const { id } = useParams();
  const [animal, setAnimal] = useState(null);

  useEffect(() => {
    async function fetchAnimal() {
      try {
        const data = await getAnimal(id);
        setAnimal(data);
      } catch (error) {
        toast.error('Failed to load animal details');
      }
    }
    fetchAnimal();
  }, [id]);

  const handleGenerateDescription = async () => {
    try {
      await generateDescription(id);
      const updatedAnimal = await getAnimal(id); // Refresh data
      setAnimal(updatedAnimal);
      toast.success('Description generated successfully');
    } catch (error) {
      toast.error('Failed to generate description');
    }
  };

  const handleGenerateTranslation = async () => {
    try {
      await generateTranslation(id);
      const updatedAnimal = await getAnimal(id); // Refresh data
      setAnimal(updatedAnimal);
      toast.success('Translation generated successfully');
    } catch (error) {
      toast.error('Failed to generate translation');
    }
  };

  if (!animal) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <Typography variant="h4">{animal.name}</Typography>
      <Paper>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Type</TableCell>
              <TableCell>{animal.animal_type}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Age</TableCell>
              <TableCell>{animal.age}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Color</TableCell>
              <TableCell>{animal.color}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Months in Shelter</TableCell>
              <TableCell>{animal.months_in_shelter}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Behavior</TableCell>
              <TableCell>{animal.behavior}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Health</TableCell>
              <TableCell>{animal.health}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Vaccinated</TableCell>
              <TableCell>{animal.vaccinated ? 'Yes' : 'No'}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Target Audience</TableCell>
              <TableCell>{animal.target_audience}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Description (EN)</TableCell>
              <TableCell>{animal.description_en || 'N/A'}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Description (NL)</TableCell>
              <TableCell>{animal.description_nl || 'N/A'}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Paper>
      {isAuthenticated() && (
        <div style={{ marginTop: '1rem' }}>
          <Button variant="contained" color="primary" onClick={handleGenerateDescription}>
            Generate Description
          </Button>
          <Button variant="contained" color="secondary" onClick={handleGenerateTranslation} style={{ marginLeft: '1rem' }}>
            Generate Translation
          </Button>
        </div>
      )}
    </div>
  );
}

export default AnimalDetail;
