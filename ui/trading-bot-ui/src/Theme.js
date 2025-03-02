import { createTheme } from '@mui/material/styles';

const monochromeTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ffffff' },
    secondary: { main: '#b0b0b0' },
    background: { default: '#000000', paper: '#1a1a1a' },
    text: { primary: '#ffffff', secondary: '#b0b0b0' },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
    fontSize: 14,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: { textTransform: 'none', color: '#ffffff', backgroundColor: '#333333', '&:hover': { backgroundColor: '#555555' } },
      },
    },
  },
});

export default monochromeTheme;
