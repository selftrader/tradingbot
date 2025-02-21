import React from 'react';
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

interface BrokerConfigProps {
  config: {
    id: number;
    broker_name: string;
    is_active: boolean;
    status: string;
    created_at: string;
  };
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  onToggleActive: (id: number) => void;
}

const BrokerConfigCard: React.FC<BrokerConfigProps> = ({
  config,
  onEdit,
  onDelete,
  onToggleActive
}) => {
  const getStatusColor = (status: string) => {
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
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6" component="div">
            {config.broker_name.toUpperCase()}
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

        <Box mt={2} display="flex" justifyContent="space-between">
          <Typography color="text.secondary" variant="body2">
            Created: {new Date(config.created_at).toLocaleString()}
          </Typography>
          <Box>
            <IconButton size="small" onClick={() => onEdit(config.id)}>
              <Edit />
            </IconButton>
            <IconButton size="small" onClick={() => onDelete(config.id)}>
              <Delete />
            </IconButton>
            <Button
              variant="outlined"
              size="small"
              onClick={() => onToggleActive(config.id)}
              startIcon={config.is_active ? <Error /> : <CheckCircle />}
              sx={{ ml: 1 }}
            >
              {config.is_active ? 'Deactivate' : 'Activate'}
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default BrokerConfigCard;