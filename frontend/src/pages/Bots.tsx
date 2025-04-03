import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  styled,
  Card,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  SmartToy as BotIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { Layout } from '../components';
import type { Bot, BotStatus } from '../types';

const StyledCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  height: '100%',
  borderRadius: theme.shape.borderRadius,
  overflow: 'hidden',
}));

const MotionBox = motion(Box);

const Bots: React.FC = () => {
  const [bots, setBots] = useState<Bot[]>([
    {
      id: 1,
      name: 'Customer Support Bot',
      description: 'Automated customer support solution',
      status: 'active' as BotStatus,
      users: 450,
      price: 29.99,
      category: 'Support',
    },
    {
      id: 2,
      name: 'News Bot',
      description: 'News aggregation and delivery',
      status: 'active' as BotStatus,
      users: 320,
      price: 19.99,
      category: 'News',
    },
    {
      id: 3,
      name: 'Shop Bot',
      description: 'E-commerce assistant',
      status: 'inactive' as BotStatus,
      users: 0,
      price: 39.99,
      category: 'E-commerce',
    },
  ]);

  const [openDialog, setOpenDialog] = useState(false);
  const [selectedBot, setSelectedBot] = useState<Bot | null>(null);

  const handleOpenDialog = (bot?: Bot) => {
    setSelectedBot(bot || null);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedBot(null);
  };

  const handleSaveBot = () => {
    // TODO: Implement save logic
    handleCloseDialog();
  };

  const handleDeleteBot = (id: number) => {
    // TODO: Implement delete logic
    setBots(bots.filter(bot => bot.id !== id));
  };

  const handleToggleStatus = (id: number) => {
    setBots(bots.map(bot => 
      bot.id === id 
        ? { ...bot, status: bot.status === 'active' ? 'inactive' : 'active' as BotStatus }
        : bot
    ));
  };

  return (
    <Layout title="Bot Management">
      <StyledCard>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Bot Management</Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon fontSize="small" />}
            onClick={() => handleOpenDialog()}
            size="small"
          >
            Add New Bot
          </Button>
        </Box>

        <TableContainer component={Paper} sx={{ boxShadow: 'none', mb: 2 }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Category</TableCell>
                <TableCell>Users</TableCell>
                <TableCell>Price</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {bots.map((bot) => (
                <TableRow key={bot.id}>
                  <TableCell>{bot.name}</TableCell>
                  <TableCell>{bot.description}</TableCell>
                  <TableCell>{bot.category}</TableCell>
                  <TableCell>{bot.users}</TableCell>
                  <TableCell>${bot.price}</TableCell>
                  <TableCell>
                    <Chip
                      label={bot.status}
                      color={bot.status === 'active' ? 'success' : 'default'}
                      size="small"
                      sx={{ height: 24, fontSize: '0.75rem' }}
                    />
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleToggleStatus(bot.id)}
                    >
                      {bot.status === 'active' ? 
                        <StopIcon fontSize="small" /> : 
                        <PlayIcon fontSize="small" />
                      }
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(bot)}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDeleteBot(bot.id)}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle>
            {selectedBot ? 'Edit Bot' : 'Add New Bot'}
          </DialogTitle>
          <DialogContent>
            <Box display="flex" flexDirection="column" gap={2} mt={2}>
              <TextField
                label="Name"
                fullWidth
                defaultValue={selectedBot?.name}
                size="small"
              />
              <TextField
                label="Description"
                fullWidth
                multiline
                rows={2}
                defaultValue={selectedBot?.description}
                size="small"
              />
              <FormControl fullWidth size="small">
                <InputLabel>Category</InputLabel>
                <Select
                  label="Category"
                  defaultValue={selectedBot?.category || ''}
                >
                  <MenuItem value="Support">Support</MenuItem>
                  <MenuItem value="News">News</MenuItem>
                  <MenuItem value="E-commerce">E-commerce</MenuItem>
                </Select>
              </FormControl>
              <TextField
                label="Price"
                type="number"
                fullWidth
                defaultValue={selectedBot?.price}
                size="small"
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} size="small">Cancel</Button>
            <Button onClick={handleSaveBot} variant="contained" color="primary" size="small">
              Save
            </Button>
          </DialogActions>
        </Dialog>
      </StyledCard>
    </Layout>
  );
};

export default Bots; 