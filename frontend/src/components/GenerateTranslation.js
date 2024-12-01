import React from 'react';
import { generateTranslation } from '../services/api';
import { useParams } from 'react-router-dom';
import { toast } from 'react-toastify';

function GenerateTranslation() {
  const { id } = useParams();

  const handleGenerate = async () => {
    try {
      await generateTranslation(id);
      toast.success('Translation generated successfully');
    } catch (error) {
      toast.error('Failed to generate description');
    }
  };

  return (
    <div>
      <h2>Generate Translation</h2>
      <button onClick={handleGenerate}>Generate translation</button>
    </div>
  );
}

export default GenerateTranslation;
