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
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Settings as SettingsIcon,
  Person as PersonIcon,
  ExitToApp as LogoutIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import styled from 'styled-components';

const drawerWidth = 240;

const Main = styled(motion.main)<{ $open: boolean }>`
  flex-grow: 1;
  padding: 24px;
  transition: margin 225ms cubic-bezier(0.4, 0, 0.6, 1) 0ms;
  margin-left: ${({ $open }) => ($open ? drawerWidth : 0)}px;
`;

const StyledAppBar = styled(AppBar)<{ $open: boolean }>`
  z-index: ${({ theme }) => theme.zIndex.drawer + 1};
  transition: width 225ms cubic-bezier(0.4, 0, 0.6, 1) 0ms;
  width: ${({ $open }) => ($open ? `calc(100% - ${drawerWidth}px)` : '100%')};
  margin-left: ${({ $open }) => ($open ? drawerWidth : 0)}px;
`;

const StyledDrawer = styled(Drawer)`
  & .MuiDrawer-paper {
    width: ${drawerWidth}px;
    box-sizing: border-box;
    background-color: ${({ theme }) => theme.palette.background.paper};
  }
`;

interface LayoutProps {
  children: React.ReactNode;
  title: string;
  isAdmin?: boolean;
}

const MotionListItem = motion(ListItem);

const Layout: React.FC<LayoutProps> = ({ children, title, isAdmin = false }) => {
  const [open, setOpen] = useState(true);
  const theme = useTheme();

  const handleDrawerToggle = () => {
    setOpen(!open);
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { text: 'Profile', icon: <PersonIcon />, path: '/profile' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
    { text: 'Logout', icon: <LogoutIcon />, path: '/logout' },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <StyledAppBar position="fixed" $open={open}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            {title}
          </Typography>
        </Toolbar>
      </StyledAppBar>

      <StyledDrawer
        variant="permanent"
        open={open}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            borderRight: `1px solid ${theme.palette.divider}`,
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <MotionListItem
                key={item.text}
                whileHover={{ x: 5 }}
                whileTap={{ scale: 0.95 }}
                sx={{ cursor: 'pointer' }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </MotionListItem>
            ))}
          </List>
          <Divider />
        </Box>
      </StyledDrawer>

      <Main $open={open}>
        <Toolbar />
        {children}
      </Main>
    </Box>
  );
};

export default Layout; 