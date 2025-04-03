import React, { useState } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
  ListItemButton,
  styled,
  Container,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Settings as SettingsIcon,
  Person as PersonIcon,
  ExitToApp as LogoutIcon,
  SmartToy as BotIcon,
  Group as UsersIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const drawerWidth = 210;

// Using MUI styled API instead of styled-components
const Main = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'open',
})<{ open?: boolean }>(({ theme, open }) => ({
  flexGrow: 1,
  padding: 0,
  transition: theme.transitions.create('margin', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  marginLeft: open ? drawerWidth : 0,
  width: open ? `calc(100% - ${drawerWidth}px)` : '100%',
}));

const StyledAppBar = styled(AppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})<{ open?: boolean }>(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  width: open ? `calc(100% - ${drawerWidth}px)` : '100%',
  marginLeft: open ? drawerWidth : 0,
  minHeight: 48,
}));

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
    backgroundColor: theme.palette.background.paper,
  },
  '& .MuiListItemIcon-root': {
    minWidth: 40,
  },
  '& .MuiListItemText-root': {
    margin: 0,
  },
  '& .MuiListItem-root': {
    padding: theme.spacing(0.5, 1),
  },
}));

// Create a motion variant of MUI ListItem
const MotionListItem = motion(ListItem);

interface LayoutProps {
  children: React.ReactNode;
  title: string;
  isAdmin?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, title, isAdmin = false }) => {
  const [open, setOpen] = useState(true);
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { logout, isAdmin: userIsAdmin } = useAuth();

  const handleDrawerToggle = () => {
    setOpen(!open);
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon fontSize="small" />, path: '/dashboard' },
    { text: 'Bots', icon: <BotIcon fontSize="small" />, path: '/bots' },
    ...(userIsAdmin ? [{ text: 'Users', icon: <UsersIcon fontSize="small" />, path: '/users' }] : []),
    { text: 'Profile', icon: <PersonIcon fontSize="small" />, path: '/profile' },
    { text: 'Settings', icon: <SettingsIcon fontSize="small" />, path: '/settings' },
    { text: 'Logout', icon: <LogoutIcon fontSize="small" />, action: handleLogout },
  ];

  const handleItemClick = (item: any) => {
    if (item.action) {
      item.action();
    } else if (item.path) {
      navigate(item.path);
    }
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <StyledAppBar position="fixed" open={open}>
        <Toolbar variant="dense" sx={{ minHeight: 48 }}>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            size="small"
            sx={{ mr: 1 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="body1" noWrap component="div" sx={{ fontWeight: 'medium' }}>
            {title}
          </Typography>
        </Toolbar>
      </StyledAppBar>

      <StyledDrawer
        variant="permanent"
        open={open}
      >
        <Toolbar variant="dense" sx={{ minHeight: 48 }} />
        <Box sx={{ overflow: 'auto' }}>
          <List dense sx={{ pt: 0.5, pb: 0.5 }}>
            {menuItems.map((item) => (
              <MotionListItem
                key={item.text}
                disablePadding
                whileHover={{ x: 3 }}
                whileTap={{ scale: 0.98 }}
                sx={{ mb: 0.5 }}
              >
                <ListItemButton
                  selected={location.pathname === item.path}
                  onClick={() => handleItemClick(item)}
                  sx={{ py: 0.5, px: 1.5 }}
                >
                  <ListItemIcon sx={{ minWidth: 36 }}>{item.icon}</ListItemIcon>
                  <ListItemText 
                    primary={item.text} 
                    primaryTypographyProps={{ fontSize: '0.9rem' }}
                  />
                </ListItemButton>
              </MotionListItem>
            ))}
          </List>
          <Divider />
        </Box>
      </StyledDrawer>

      <Main open={open} component={motion.div}>
        <Toolbar variant="dense" sx={{ minHeight: 48 }} />
        <Box sx={{ width: '100%' }}>
          {children}
        </Box>
      </Main>
    </Box>
  );
};

export default Layout; 