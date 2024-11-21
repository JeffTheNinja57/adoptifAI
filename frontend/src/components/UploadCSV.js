import React, { useState } from 'react';
import { uploadCSV } from '../services/api';
import { toast } from 'react-toastify';
import { Button, Input } from '@mui/material';

function UploadCSV() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
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
    <div className="upload-csv">
      <h2>Upload CSV</h2>
      <Input
        type="file"
        inputProps={{ accept: '.csv' }}
        onChange={(e) => setFile(e.target.files[0])}
      />
      <Button variant="contained" color="primary" onClick={handleUpload}>
        Upload
      </Button>
    </div>
  );
}

export default UploadCSV;
