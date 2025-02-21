// frontend/src/components/LiveUpdates.js
import React, { useState, useEffect } from 'react';
import { tradingAPI } from '../services/api';
import { useWebSocket } from '../hooks/useWebSocket';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Typography
} from '@mui/material';

const LiveUpdates = ({ symbol }) => {
    const [trades, setTrades] = useState([]);
    const [isTrading, setIsTrading] = useState(false);
    const { lastMessage } = useWebSocket(`ws://localhost:8000/ws/trades/${symbol}`);

    useEffect(() => {
        checkTradingStatus();
    }, [symbol]);

    const checkTradingStatus = async () => {
        try {
            const status = await tradingAPI.getTradeStatus(symbol);
            setIsTrading(status.active);
        } catch (error) {
            console.error('Failed to get trading status:', error);
        }
    };

    const handleStartTrading = async () => {
        try {
            await tradingAPI.startTrading(symbol);
            setIsTrading(true);
        } catch (error) {
            console.error('Failed to start trading:', error);
        }
    };

    const handleStopTrading = async () => {
        try {
            await tradingAPI.stopTrading(symbol);
            setIsTrading(false);
        } catch (error) {
            console.error('Failed to stop trading:', error);
        }
    };

    return (
        <TableContainer component={Paper} sx={{ marginTop: 4, maxWidth: '100%' }}>
            <Typography variant="h6" align="center" gutterBottom>
                Live Trade Updates
            </Typography>
            <Table sx={{ minWidth: 650 }} aria-label="live trade updates table">
                <TableHead>
                    <TableRow>
                        <TableCell>Time</TableCell>
                        <TableCell>Symbol</TableCell>
                        <TableCell>Action</TableCell>
                        <TableCell>Quantity</TableCell>
                        <TableCell>Entry Price</TableCell>
                        <TableCell>P&L</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {trades.map((trade, index) => (
                        <TableRow key={index}>
                            <TableCell>{trade.trade_time}</TableCell>
                            <TableCell>{trade.symbol}</TableCell>
                            <TableCell>{trade.action}</TableCell>
                            <TableCell>{trade.quantity}</TableCell>
                            <TableCell>{trade.entry_price}</TableCell>
                            <TableCell>{trade.current_pl}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default LiveUpdates;
