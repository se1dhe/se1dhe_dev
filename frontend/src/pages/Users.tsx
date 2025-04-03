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
  Avatar,
  styled,
  Card,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Lock as LockIcon,
  LockOpen as UnlockIcon,
  Person as PersonIcon,
  Block as BlockIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { Layout } from '../components';
import type { User, UserRole, UserStatus } from '../types';

const StyledCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  height: '100%',
  borderRadius: theme.shape.borderRadius,
  overflow: 'hidden',
}));

const MotionBox = motion(Box);

const Users: React.FC = () => {
  const [users, setUsers] = useState<User[]>([
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      role: 'admin',
      status: 'active',
      telegramUsername: '@johndoe',
      createdAt: '2024-01-01',
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane@example.com',
      role: 'user',
      status: 'active',
      telegramUsername: '@janesmith',
      createdAt: '2024-01-15',
    },
    {
      id: 3,
      name: 'Bob Johnson',
      email: 'bob@example.com',
      role: 'user',
      status: 'inactive',
      createdAt: '2024-02-01',
    },
  ]);

  const [openDialog, setOpenDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const handleOpenDialog = (user?: User) => {
    setSelectedUser(user || null);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedUser(null);
  };

  const handleSaveUser = () => {
    // TODO: Implement save logic
    handleCloseDialog();
  };

  const handleDeleteUser = (id: number) => {
    // TODO: Implement delete logic
    setUsers(users.filter(user => user.id !== id));
  };

  const handleToggleStatus = (id: number) => {
    setUsers(users.map(user => 
      user.id === id 
        ? { ...user, status: user.status === 'active' ? 'inactive' : 'active' }
        : user
    ));
  };

  return (
    <Layout title="User Management">
      <StyledCard>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">User Management</Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon fontSize="small" />}
            onClick={() => handleOpenDialog()}
            size="small"
          >
            Add New User
          </Button>
        </Box>

        <TableContainer component={Paper} sx={{ boxShadow: 'none', mb: 2 }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>User</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Role</TableCell>
                <TableCell>Telegram</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>
                    <Box display="flex" alignItems="center">
                      <Avatar sx={{ mr: 1, width: 24, height: 24, fontSize: '0.8rem' }}>
                        {user.name.charAt(0)}
                      </Avatar>
                      {user.name}
                    </Box>
                  </TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <Chip
                      label={user.role}
                      color={user.role === 'admin' ? 'primary' : 'default'}
                      size="small"
                      sx={{ height: 24, fontSize: '0.75rem' }}
                    />
                  </TableCell>
                  <TableCell>{user.telegramUsername || '-'}</TableCell>
                  <TableCell>
                    <Chip
                      label={user.status}
                      color={user.status === 'active' ? 'success' : 'default'}
                      size="small"
                      sx={{ height: 24, fontSize: '0.75rem' }}
                    />
                  </TableCell>
                  <TableCell>{user.createdAt}</TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleToggleStatus(user.id)}
                    >
                      {user.status === 'active' ? 
                        <LockIcon fontSize="small" /> : 
                        <UnlockIcon fontSize="small" />
                      }
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(user)}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDeleteUser(user.id)}
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
            {selectedUser ? 'Edit User' : 'Add New User'}
          </DialogTitle>
          <DialogContent>
            <Box display="flex" flexDirection="column" gap={2} mt={2}>
              <TextField
                label="Name"
                fullWidth
                defaultValue={selectedUser?.name}
                size="small"
              />
              <TextField
                label="Email"
                type="email"
                fullWidth
                defaultValue={selectedUser?.email}
                size="small"
              />
              <FormControl fullWidth size="small">
                <InputLabel>Role</InputLabel>
                <Select
                  label="Role"
                  defaultValue={selectedUser?.role || 'user'}
                >
                  <MenuItem value="admin">Admin</MenuItem>
                  <MenuItem value="user">User</MenuItem>
                </Select>
              </FormControl>
              <TextField
                label="Telegram Username"
                fullWidth
                defaultValue={selectedUser?.telegramUsername}
                size="small"
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} size="small">Cancel</Button>
            <Button onClick={handleSaveUser} variant="contained" color="primary" size="small">
              Save
            </Button>
          </DialogActions>
        </Dialog>
      </StyledCard>
    </Layout>
  );
};

export default Users; 