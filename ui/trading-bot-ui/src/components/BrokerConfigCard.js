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
import { Edit, Delete, CheckCircle, Error } from '@mui/icons-material';

const BrokerConfigCard = ({ config, onEdit, onDelete, onToggleActive }) => {
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
        {/* Header: Username and Status Chips */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ fontWeight: 'bold', color: '#fff' }}
          >
            recscse
          </Typography>
          <Box>
            <Chip
              label={config.status}
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

        {/* Body: Created date and Action Buttons */}
        <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
          <Typography color="text.secondary" variant="body2">
            Created: {new Date(config.created_at).toLocaleString()}
          </Typography>
          <Box>
            <IconButton 
              size="small" 
              onClick={() => onEdit(config.id)} 
              color="inherit"
              sx={{ color: '#fff' }}
            >
              <Edit />
            </IconButton>
            <IconButton 
              size="small" 
              onClick={() => onDelete(config.id)} 
              color="inherit"
              sx={{ color: '#fff' }}
            >
              <Delete />
            </IconButton>
            <Button
              variant="outlined"
              size="small"
              onClick={() => onToggleActive(config.id)}
              startIcon={config.is_active ? <Error /> : <CheckCircle />}
              sx={{ ml: 1, borderColor: '#fff', color: '#fff' }}
            >
              {config.is_active ? 'Deactivate' : 'Activate'}
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

BrokerConfigCard.propTypes = {
  config: PropTypes.shape({
    id: PropTypes.number.isRequired,
    status: PropTypes.string.isRequired,
    is_active: PropTypes.bool.isRequired,
    created_at: PropTypes.string.isRequired,
  }).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onToggleActive: PropTypes.func.isRequired,
};

export default BrokerConfigCard;