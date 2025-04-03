import React from 'react';
import { Box, Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button } from '@mui/material';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import Layout from '../components/Layout';

const StyledPaper = styled(Paper)`
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

const MotionBox = motion(Box);

const AdminDashboard: React.FC = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
    },
  };

  // Example data - replace with real data from API
  const users = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'User' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'Admin' },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'User' },
  ];

  return (
    <Layout title="Admin Dashboard" isAdmin>
      <MotionBox variants={containerVariants} initial="hidden" animate="visible">
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr', lg: '1fr 1fr 1fr 1fr' }, gap: 3, mb: 4 }}>
          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                Total Users
              </Typography>
              <Typography variant="h4" color="primary">
                1,234
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Active users in the system
              </Typography>
            </StyledPaper>
          </MotionBox>

          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                System Status
              </Typography>
              <Typography variant="h4" color="success.main">
                Online
              </Typography>
              <Typography variant="body2" color="text.secondary">
                All systems operational
              </Typography>
            </StyledPaper>
          </MotionBox>

          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <Typography variant="h4" color="info.main">
                89
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Actions in the last 24h
              </Typography>
            </StyledPaper>
          </MotionBox>

          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                System Load
              </Typography>
              <Typography variant="h4" color="warning.main">
                45%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Current system utilization
              </Typography>
            </StyledPaper>
          </MotionBox>
        </Box>

        <MotionBox variants={itemVariants}>
          <StyledPaper>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                User Management
              </Typography>
              <Button variant="contained" color="primary">
                Add User
              </Button>
            </Box>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell>Role</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {users.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>{user.name}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>{user.role}</TableCell>
                      <TableCell>
                        <Button size="small" color="primary" sx={{ mr: 1 }}>
                          Edit
                        </Button>
                        <Button size="small" color="error">
                          Delete
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </StyledPaper>
        </MotionBox>
      </MotionBox>
    </Layout>
  );
};

export default AdminDashboard; 