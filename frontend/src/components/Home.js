// src/components/Home.js

import React from 'react';
import { Button } from '@mui/material';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home">
      <h1>Welcome to Adopt-if-AI</h1>
      <p>Your platform to help animals find a loving home.</p>
      <Button variant="contained" color="primary" component={Link} to="/animals">
        View Animals
      </Button>
    </div>
  );
}

export default Home;
