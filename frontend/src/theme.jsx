// src/theme.js

import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2A3663', // Dark blue
    },
    secondary: {
      main: '#B59F78', // Brownish
    },
    background: {
      default: '#FAF6E3', // Light beige
      paper: '#D8DBBD', // Light greenish
    },
    text: {
      primary: '#2A3663',
      secondary: '#B59F78',
    },
  },
});

export default theme;
