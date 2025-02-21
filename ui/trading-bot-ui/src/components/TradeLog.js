import React, { useEffect, useState } from 'react';
import { Typography, Paper } from '@mui/material';
import { subscribeToTradeUpdates } from '../services/api';

const TradeLog = () => {
    const [log, setLog] = useState([]);

    useEffect(() => {
        const unsubscribe = subscribeToTradeUpdates((update) => {
            setLog(prevLog => [update, ...prevLog]);
        });
        return unsubscribe;
    }, []);

    return (
        <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6">Trade Log</Typography>
            {log.length > 0 ? log.map((entry, idx) => (
                <Typography key={idx} variant="body2">
                    {entry.message} at {entry.time}
                </Typography>
            )) : (
                <Typography variant="body1">No trade updates yet.</Typography>
            )}
        </Paper>
    );
};

export default TradeLog;
