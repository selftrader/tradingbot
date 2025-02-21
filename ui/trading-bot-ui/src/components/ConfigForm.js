import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Typography, Grid } from '@mui/material';
import { tradingAPI } from '../services/api';

const ConfigForm = ({ broker }) => {
  const [config, setConfig] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const data = await tradingAPI.getBrokerConfig();
      setConfig(data);
      setError(null);
    } catch (err) {
      setError('Failed to load configuration');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      await tradingAPI.saveBrokerConfig(config);
      setError(null);
    } catch (err) {
      setError('Failed to save configuration');
    } finally {
      setIsLoading(false);
    }
  };

  if (!broker) return null;

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        {broker} Configuration
      </Typography>
      <Grid container spacing={2}>
        {broker === 'Upstocks' ? (
          <>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Client ID"
                name="clientId"
                value={config?.clientId || ''}
                onChange={handleChange}
                placeholder="Enter your Client ID"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Client Secret"
                name="clientSecret"
                type="password"
                value={config?.clientSecret || ''}
                onChange={handleChange}
                placeholder="Enter your Client Secret"
              />
            </Grid>
          </>
        ) : (
          <>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Auth URL"
                name="authUrl"
                value={config?.authUrl || ''}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Token URL"
                name="tokenUrl"
                value={config?.tokenUrl || ''}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Client ID"
                name="clientId"
                value={config?.clientId || ''}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Client Secret"
                name="clientSecret"
                type="password"
                value={config?.clientSecret || ''}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Redirect URI"
                name="redirectUri"
                value={config?.redirectUri || ''}
                onChange={handleChange}
              />
            </Grid>
          </>
        )}
      </Grid>
      <Button variant="contained" type="submit" sx={{ mt: 2 }} disabled={isLoading}>
        {isLoading ? 'Saving...' : 'Save Configuration'}
      </Button>
      {error && (
        <Typography variant="body2" color="error" sx={{ mt: 1 }}>
          {error}
        </Typography>
      )}
    </Box>
  );
};

export default ConfigForm;