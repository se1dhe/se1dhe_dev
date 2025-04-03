import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from './theme/theme';
import Login from './pages/Login';
import UserDashboard from './pages/UserDashboard';
import AdminDashboard from './pages/AdminDashboard';
import { AuthProvider, useAuth } from './contexts/AuthContext';

const AppRoutes: React.FC = () => {
  const { isAuthenticated, isAdmin } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={
        isAuthenticated ? <Navigate to="/dashboard" /> : <Login />
      } />
      <Route path="/dashboard" element={
        isAuthenticated ? (
          isAdmin ? <AdminDashboard /> : <UserDashboard />
        ) : (
          <Navigate to="/login" />
        )
      } />
      <Route path="/" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <AppRoutes />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
