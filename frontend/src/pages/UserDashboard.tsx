import React from 'react';
import { Box, Paper, Typography } from '@mui/material';
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

const UserDashboard: React.FC = () => {
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

  return (
    <Layout title="User Dashboard">
      <MotionBox variants={containerVariants} initial="hidden" animate="visible">
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr', lg: '1fr 1fr 1fr 1fr' }, gap: 3 }}>
          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                Welcome Back
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Here's what's happening with your account today.
              </Typography>
            </StyledPaper>
          </MotionBox>

          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Access your most used features here.
              </Typography>
            </StyledPaper>
          </MotionBox>

          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Your latest actions and updates.
              </Typography>
            </StyledPaper>
          </MotionBox>

          <MotionBox variants={itemVariants}>
            <StyledPaper>
              <Typography variant="h6" gutterBottom>
                Notifications
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Stay updated with your latest notifications.
              </Typography>
            </StyledPaper>
          </MotionBox>
        </Box>
      </MotionBox>
    </Layout>
  );
};

export default UserDashboard; 