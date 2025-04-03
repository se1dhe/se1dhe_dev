import React from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  Card,
  CardContent,
  Avatar,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  ListItemSecondaryAction,
  Chip,
  IconButton,
  Divider,
  useTheme,
  styled,
} from '@mui/material';
import {
  SmartToy as BotIcon,
  Person as PersonIcon,
  MonetizationOn as MoneyIcon,
  Message as MessageIcon,
  MoreVert as MoreIcon,
  ArrowForward as ArrowForwardIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';

// Create motion variants of MUI components
const MotionCard = motion(Card);
const MotionBox = motion(Box);

// Styled components
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  borderRadius: 8,
  boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
}));

const StatCard = styled(Card)(({ theme }) => ({
  height: '100%',
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
  borderRadius: 8,
  background: theme.palette.background.paper,
  textAlign: 'center',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
}));

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  // Define the statistics for the dashboard
  const stats = [
    {
      title: 'Total Bots',
      value: '12',
      icon: <BotIcon sx={{ fontSize: 28 }} />,
      color: theme.palette.primary.main,
    },
    {
      title: 'Active Users',
      value: '143',
      icon: <PersonIcon sx={{ fontSize: 28 }} />,
      color: theme.palette.success.main,
    },
    {
      title: 'Revenue',
      value: '$1,240',
      icon: <MoneyIcon sx={{ fontSize: 28 }} />,
      color: theme.palette.warning.main,
    },
    {
      title: 'Messages',
      value: '5,732',
      icon: <MessageIcon sx={{ fontSize: 28 }} />,
      color: theme.palette.info.main,
    },
  ];

  // Define dummy data for recent bots
  const recentBots = [
    { 
      id: 1, 
      name: 'Support Agent', 
      users: 45, 
      status: 'active',
      avatar: 'S'
    },
    { 
      id: 2, 
      name: 'Sales Assistant', 
      users: 32, 
      status: 'maintenance',
      avatar: 'SA' 
    },
    { 
      id: 3, 
      name: 'Booking Service', 
      users: 28, 
      status: 'active',
      avatar: 'B' 
    },
  ];

  // Status colors for bot status chips
  const statusColors: Record<string, any> = {
    active: { color: 'success', label: 'Active' },
    maintenance: { color: 'warning', label: 'Maintenance' },
    inactive: { color: 'error', label: 'Inactive' },
  };

  return (
    <Layout title="Dashboard">
      <Box sx={{ p: { xs: 2, sm: 3 } }}>
        <Grid container spacing={3}>
          {/* Statistics Cards */}
          {stats.map((stat, index) => (
            <Grid item xs={6} sm={3} key={index}>
              <MotionBox
                whileHover={{ scale: 1.03 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                sx={{ height: '100%' }}
              >
                <StatCard>
                  <CardContent sx={{ p: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                    <Avatar 
                      sx={{ 
                        bgcolor: `${stat.color}15`, 
                        color: stat.color,
                        mb: 1.5,
                        width: 50,
                        height: 50
                      }}
                    >
                      {stat.icon}
                    </Avatar>
                    <Typography variant="h3" sx={{ fontWeight: 'bold', mb: 0.5, fontSize: '1.5rem' }}>
                      {stat.value}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.9rem' }}>
                      {stat.title}
                    </Typography>
                  </CardContent>
                </StatCard>
              </MotionBox>
            </Grid>
          ))}

          {/* Recent Bots and Quick Actions */}
          <Grid item xs={12} md={8}>
            <StyledPaper elevation={0}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h5" sx={{ fontWeight: 'medium' }}>
                  Recent Bots
                </Typography>
                <Button 
                  size="small" 
                  endIcon={<ArrowForwardIcon />}
                  onClick={() => navigate('/bots')}
                >
                  View All
                </Button>
              </Box>
              <List>
                {recentBots.map((bot, index) => (
                  <React.Fragment key={bot.id}>
                    <ListItem 
                      component={motion.div}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.2 + index * 0.1 }}
                      sx={{ px: 1, py: 1.5 }}
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: theme.palette.primary.main }}>
                          {bot.avatar}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText 
                        primary={bot.name}
                        secondary={`${bot.users} active users`}
                        primaryTypographyProps={{ 
                          fontWeight: 'medium',
                          variant: 'body1' 
                        }}
                        secondaryTypographyProps={{ 
                          variant: 'body2'
                        }}
                      />
                      <ListItemSecondaryAction>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Chip 
                            size="small" 
                            label={statusColors[bot.status].label}
                            color={statusColors[bot.status].color}
                            sx={{ mr: 1 }}
                          />
                          <IconButton size="small">
                            <MoreIcon fontSize="small" />
                          </IconButton>
                        </Box>
                      </ListItemSecondaryAction>
                    </ListItem>
                    {index < recentBots.length - 1 && <Divider variant="inset" component="li" />}
                  </React.Fragment>
                ))}
              </List>
            </StyledPaper>
          </Grid>

          {/* Activity Summary */}
          <Grid item xs={12} md={4}>
            <StyledPaper elevation={0}>
              <Typography variant="h5" sx={{ fontWeight: 'medium', mb: 2 }}>
                Quick Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                <Button 
                  variant="outlined" 
                  fullWidth 
                  startIcon={<BotIcon />}
                  onClick={() => navigate('/bots/new')}
                >
                  Create New Bot
                </Button>
                <Button 
                  variant="outlined" 
                  fullWidth 
                  startIcon={<PersonIcon />}
                  onClick={() => navigate('/users')}
                >
                  Manage Users
                </Button>
                <Button 
                  variant="outlined" 
                  fullWidth 
                  startIcon={<MoneyIcon />}
                >
                  View Revenue
                </Button>
              </Box>
            </StyledPaper>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
};

export default Dashboard; 