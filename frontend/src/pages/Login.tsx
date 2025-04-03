import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Container,
  Alert,
} from '@mui/material';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const StyledPaper = styled(Paper)`
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  max-width: 400px;
  width: 100%;
`;

const Form = styled.form`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const MotionContainer = motion(Container);
const MotionPaper = motion(StyledPaper);
const MotionTypography = motion(Typography);
const MotionBox = motion(Box);

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <MotionContainer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <MotionPaper
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <MotionTypography
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
          variant="h4"
          gutterBottom
        >
          Welcome Back
        </MotionTypography>
        
        <MotionTypography
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          variant="body2"
          color="text.secondary"
          sx={{ mb: 2 }}
        >
          Please sign in to continue
        </MotionTypography>

        {error && (
          <Alert severity="error" sx={{ width: '100%' }}>
            {error}
          </Alert>
        )}

        <Form onSubmit={handleSubmit}>
          <MotionBox
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <TextField
              fullWidth
              label="Email"
              variant="outlined"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
            />
          </MotionBox>

          <MotionBox
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <TextField
              fullWidth
              label="Password"
              type="password"
              variant="outlined"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
            />
          </MotionBox>

          <MotionBox
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.7 }}
          >
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              size="large"
              disabled={isLoading}
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>
          </MotionBox>
        </Form>
      </MotionPaper>
    </MotionContainer>
  );
};

export default Login; 