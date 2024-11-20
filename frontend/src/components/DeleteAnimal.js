import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { deleteAnimal } from '../services/api';
import { toast } from 'react-toastify';

function DeleteAnimal() {
  const { id } = useParams();
  const navigate = useNavigate();

  const handleDelete = async () => {
    try {
      await deleteAnimal(id);
      toast.success('Animal deleted successfully');
      navigate('/animals');
    } catch (error) {
      toast.error('Failed to delete animal');
    }
  };

  return (
    <div>
      <h2>Delete Animal</h2>
      <p>Are you sure you want to delete this animal?</p>
      <button onClick={handleDelete}>Yes, Delete</button>
      <button onClick={() => navigate(-1)}>Cancel</button>
    </div>
  );
}

export default DeleteAnimal;
