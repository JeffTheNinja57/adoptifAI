import React, { useState } from 'react';
import { addAnimal } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

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
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addAnimal(formData);
      toast.success('Animal added successfully');
      navigate('/animals');
    } catch (error) {
      toast.error('Failed to add animal');
    }
  };

  return (
    <div className="form-container">
      <h2>Add New Animal</h2>
      <form onSubmit={handleSubmit}>
        {/* Input fields for animal data */}
        <input
          type="text"
          placeholder="Name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
        {/* Other input fields */}
        {/* ... */}
        <button type="submit">Add Animal</button>
      </form>
    </div>
  );
}

export default AddAnimal;
