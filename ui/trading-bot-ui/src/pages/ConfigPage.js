import React, { useState, useEffect } from 'react';
import {
    Container,
    Paper,
    TextField,
    Button,
    Typography,
    Alert,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    List,
    ListItem,
    ListItemText,
    Divider,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions
} from '@mui/material';
import { tradingAPI } from '../services/api';

const brokerOptions = [
    { value: 'dhan', label: 'Dhan' },
    { value: 'zerodha', label: 'Zerodha' },
    { value: 'upstocks', label: 'Upstocks' },
    { value: 'angel', label: 'Angel' },
    { value: 'fyer', label: 'Fyer' }
];

const ConfigPage = ({ user }) => {
    const [selectedBroker, setSelectedBroker] = useState('');
    const [config, setConfig] = useState({
        brokerName: '',
        apiKey: '',
        secretKey: '',
        baseUrl: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [brokerAccounts, setBrokerAccounts] = useState([]);
    const [open, setOpen] = useState(false);

    // Fetch list of stored broker accounts for the logged-in user
    const fetchBrokerAccounts = async () => {
        try {
            const accounts = await tradingAPI.getBrokerConfigs({ userId: user?.id });
            setBrokerAccounts(accounts);
        } catch (err) {
            console.error('Error fetching broker accounts:', err);
        }
    };

    useEffect(() => {
        if (user) fetchBrokerAccounts();
    }, [user, success]);

    const handleBrokerChange = (e) => {
        const selected = e.target.value;
        setSelectedBroker(selected);
        if (selected === 'dhan') {
            setConfig({
                brokerName: 'Dhan',
                apiKey: 'API_KEY_DHAN',
                secretKey: 'SECRET_DHAN',
                baseUrl: 'https://api.dhan.com'
            });
        } else if (selected === 'zerodha') {
            setConfig({
                brokerName: 'Zerodha',
                apiKey: 'API_KEY_ZERODHA',
                secretKey: 'SECRET_ZERODHA',
                baseUrl: 'https://api.zerodha.com'
            });
        } else if (selected === 'upstocks') {
            setConfig({
                brokerName: 'Upstocks',
                apiKey: 'API_KEY_UPSTOCKS',
                secretKey: 'SECRET_UPSTOCKS',
                baseUrl: 'https://api.upstocks.com'
            });
        } else if (selected === 'angel') {
            setConfig({
                brokerName: 'Angel',
                apiKey: 'API_KEY_ANGEL',
                secretKey: 'SECRET_ANGEL',
                baseUrl: 'https://api.angelbroking.com'
            });
        } else if (selected === 'fyer') {
            setConfig({
                brokerName: 'Fyer',
                apiKey: 'API_KEY_FYER',
                secretKey: 'SECRET_FYER',
                baseUrl: 'https://api.fyer.in'
            });
        } else {
            setConfig({
                brokerName: '',
                apiKey: '',
                secretKey: '',
                baseUrl: ''
            });
        }
    };

    const handleChange = (e) => {
        setConfig({ ...config, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');
        try {
            // Include the user ID in the payload.
            await tradingAPI.saveBrokerConfig({ ...config, userId: user.id });
            setSuccess('Broker configuration saved successfully!');
            setOpen(false);
        } catch (err) {
            console.error('Error saving broker configuration:', err);
            setError('Failed to save configuration. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleAddAccountClick = () => {
        setSelectedBroker('');
        setConfig({
            brokerName: '',
            apiKey: '',
            secretKey: '',
            baseUrl: ''
        });
        setError('');
        setSuccess('');
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <Container sx={{ mt: 4 }}>
            <Paper sx={{ p: 3, mb: 4 }}>
                <Typography variant="h5" gutterBottom>
                    Stored Broker Accounts ({brokerAccounts.length})
                </Typography>
                <Divider sx={{ mb: 2 }} />
                {brokerAccounts.length > 0 ? (
                    <List>
                        {brokerAccounts.map((account, idx) => (
                            <ListItem key={idx}>
                                <ListItemText
                                    primary={account.brokerName}
                                    secondary={`API Key: ${account.apiKey} | Base URL: ${account.baseUrl}`}
                                />
                            </ListItem>
                        ))}
                    </List>
                ) : (
                    <Typography variant="body1">
                        No broker accounts added yet.
                    </Typography>
                )}
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleAddAccountClick}
                    sx={{ mt: 2 }}
                >
                    Add Account
                </Button>
            </Paper>
            <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
                <DialogTitle>Configure Broker Account</DialogTitle>
                <DialogContent>
                    <FormControl fullWidth sx={{ mb: 2, mt: 1 }}>
                        <InputLabel id="broker-select-label">Select Broker</InputLabel>
                        <Select
                            labelId="broker-select-label"
                            value={selectedBroker}
                            label="Select Broker"
                            onChange={handleBrokerChange}
                        >
                            {brokerOptions.map((broker) => (
                                <MenuItem key={broker.value} value={broker.value}>
                                    {broker.label}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                    {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
                    {selectedBroker && (
                        <form id="brokerForm" onSubmit={handleSubmit}>
                            <TextField
                                fullWidth
                                margin="normal"
                                name="brokerName"
                                label="Broker Name"
                                variant="outlined"
                                value={config.brokerName}
                                onChange={handleChange}
                            />
                            <TextField
                                fullWidth
                                margin="normal"
                                name="apiKey"
                                label="API Key"
                                variant="outlined"
                                value={config.apiKey}
                                onChange={handleChange}
                            />
                            <TextField
                                fullWidth
                                margin="normal"
                                name="secretKey"
                                label="Secret Key"
                                variant="outlined"
                                value={config.secretKey}
                                onChange={handleChange}
                            />
                            <TextField
                                fullWidth
                                margin="normal"
                                name="baseUrl"
                                label="Base URL"
                                variant="outlined"
                                value={config.baseUrl}
                                onChange={handleChange}
                            />
                        </form>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Cancel</Button>
                    <Button
                        type="submit"
                        form="brokerForm"
                        variant="contained"
                        color="primary"
                        disabled={loading}
                    >
                        {loading ? 'Saving...' : 'Save Configuration'}
                    </Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
};

export default ConfigPage;