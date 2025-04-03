import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00ff9d',
      light: '#6effd1',
      dark: '#00cb6e',
    },
    secondary: {
      main: '#ff3366',
      light: '#ff6b8f',
      dark: '#c6003d',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b3b3b3',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Consolas", "Monaco", monospace',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      letterSpacing: '0.02em',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      letterSpacing: '0.02em',
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      letterSpacing: '0.02em',
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.7,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '8px 24px',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
        },
      },
    },
  },
}); 