// src/components/UploadCSV.js

import React, {useState} from 'react';
import {uploadCSV} from '../services/api';
import {toast} from 'react-toastify';
import {Button, Input, Paper, Typography} from '@mui/material';

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
        <Paper className="form-container" style={{padding: '2rem', marginTop: '2rem'}}>
            <Typography variant="h5" gutterBottom>
                Upload CSV
            </Typography>
            <Input
                type="file"
                inputProps={{accept: '.csv'}}
                onChange={(e) => setFile(e.target.files[0])}
                fullWidth
            />
            <Button variant="contained" color="primary" onClick={handleUpload} style={{marginTop: '1rem'}}>
                Upload
            </Button>
        </Paper>
    );
}

export default UploadCSV;
