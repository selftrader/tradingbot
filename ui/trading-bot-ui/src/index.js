import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { ThemeProvider, CssBaseline } from '@mui/material';
import monochromeTheme from './Theme';

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
    <React.StrictMode>
        <ThemeProvider theme={monochromeTheme}>
            <CssBaseline />
            <App />
        </ThemeProvider>
    </React.StrictMode>
);