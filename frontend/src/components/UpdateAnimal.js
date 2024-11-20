import React, { useEffect, useState } from 'react';
import { updateAnimal, getAnimal } from '../services/api';
import { useNavigate, useParams } from 'react-router-dom';
import { toast } from 'react-toastify';

function UpdateAnimal() {
  const { id } = useParams();
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
        setFormData(data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchAnimal();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateAnimal(id, formData);
      toast.success('Animal updated successfully');
      navigate(`/animals/${id}`);
    } catch (error) {
      toast.error('Failed to update animal');
    }
  };

  return (
    <div className="form-container">
      <h2>Update Animal</h2>
      <form onSubmit={handleSubmit}>
        {/* Input fields for animal data with existing values */}
        {/* ... */}
        <button type="submit">Update Animal</button>
      </form>
    </div>
  );
}

export default UpdateAnimal;
