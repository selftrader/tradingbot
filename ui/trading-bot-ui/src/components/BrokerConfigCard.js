import React from 'react';
import PropTypes from 'prop-types';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  IconButton,
  Box,
  Button
} from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';

const BrokerConfigCard = ({ config, onEdit, onDelete, onToggleActive }) => {
  // ✅ Determine Status Color Dynamically
  const getStatusColor = (status) => {
    switch (status) {
      case 'connected':
        return 'success';
      case 'error':
        return 'error';
      default:
        return 'warning';
    }
  };

  return (
    <Card sx={{ 
      mb: 2, 
      backgroundColor: '#1d1d1d', 
      borderRadius: 2, 
      boxShadow: 3, 
      border: '1px solid #333' 
    }}>
      <CardContent>
        {/* ✅ Header: Username and Status Chips */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ fontWeight: 'bold', color: '#fff' }}
          >
            {config.username || "Unknown User"} {/* ✅ Fix for dynamic username */}
          </Typography>
          <Box>
            <Chip
              label={config.status || "Unknown"}
              color={getStatusColor(config.status)}
              size="small"
              sx={{ mr: 1 }}
            />
            <Chip
              label={config.is_active ? 'Active' : 'Inactive'}
              color={config.is_active ? 'primary' : 'default'}
              size="small"
            />
          </Box>
        </Box>

        {/* ✅ Body: Created Date and Action Buttons */}
        <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
          <Typography color="text.secondary" variant="body2">
            Created: {config.created_at ? new Date(config.created_at).toLocaleString() : "N/A"} {/* ✅ Fix for missing date */}
          </Typography>
          <Box>
            <IconButton 
              size="small" 
              onClick={() => onEdit(config)}  // ✅ Fix: Pass full config instead of just ID
              color="inherit"
              sx={{ color: '#fff' }}
            >
              <Edit />
            </IconButton>
            <IconButton 
              size="small" 
              onClick={() => onDelete(config)}  // ✅ Fix: Pass full config
              color="error"
              sx={{ color: '#fff' }}
            >
              <Delete />
            </IconButton>
            <Button 
              variant="contained" 
              color={config.is_active ? "secondary" : "primary"}
              onClick={() => onToggleActive(config)}
              size="small"
              sx={{ ml: 1 }}
            >
              {config.is_active ? "Deactivate" : "Activate"}
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

// ✅ Define PropTypes for Type Safety
BrokerConfigCard.propTypes = {
  config: PropTypes.shape({
    id: PropTypes.number.isRequired,
    username: PropTypes.string,
    status: PropTypes.string,
    is_active: PropTypes.bool.isRequired,
    created_at: PropTypes.string
  }).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onToggleActive: PropTypes.func.isRequired,
};

export default BrokerConfigCard;
