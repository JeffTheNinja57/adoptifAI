import React from 'react';
import { generateDescription } from '../services/api';
import { useParams } from 'react-router-dom';
import { toast } from 'react-toastify';

function GenerateDescription() {
  const { id } = useParams();

  const handleGenerate = async () => {
    try {
      await generateDescription(id);
      toast.success('Description generated successfully');
    } catch (error) {
      toast.error('Failed to generate description');
    }
  };

  return (
    <div>
      <h2>Generate Description</h2>
      <button onClick={handleGenerate}>Generate Description</button>
    </div>
  );
}

export default GenerateDescription;
