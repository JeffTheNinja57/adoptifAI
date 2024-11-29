import {createTheme} from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: {
            main: '#C0C78C',
        },
        secondary: {

            main: '#A5B68D',
        },
        background: {
            default: '#FCFAEE', // Light background
            paper: '#A5B68D', // Muted green
        },
        text: {
            primary: '#2D2D2D', // Dark color for contrast on 'paper' background
            secondary: '#FCFAEE', // Light color for contrast on dark elements
        },
    },
});

export default theme;
