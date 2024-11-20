import React, { useState } from 'react';
import { uploadCSV } from '../services/api';
import { toast } from 'react-toastify';

function UploadCSV() {
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      toast.error('Please select a CSV file');
      return;
    }
    try {
      await uploadCSV(file);
      toast.success('CSV uploaded successfully');
    } catch (error) {
      toast.error('Failed to upload CSV');
    }
  };

  return (
    <div className="form-container">
      <h2>Upload CSV</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default UploadCSV;
