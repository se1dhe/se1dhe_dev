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
    fontSize: 14,
    h1: {
      fontSize: '2rem',
      fontWeight: 600,
      letterSpacing: '0.02em',
    },
    h2: {
      fontSize: '1.75rem',
      fontWeight: 600,
      letterSpacing: '0.02em',
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      letterSpacing: '0.02em',
    },
    h4: {
      fontSize: '1.3rem',
      fontWeight: 600,
    },
    h5: {
      fontSize: '1.1rem',
      fontWeight: 600,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
    },
    body1: {
      fontSize: '0.95rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
      fontSize: '0.875rem',
    },
    caption: {
      fontSize: '0.8rem',
    },
  },
  shape: {
    borderRadius: 6,
  },
  spacing: 8,
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          padding: '6px 16px',
        },
        sizeSmall: {
          padding: '4px 10px',
          fontSize: '0.8rem',
        },
      },
      defaultProps: {
        size: 'small',
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          boxShadow: '0 3px 10px rgba(0, 0, 0, 0.2)',
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          padding: '8px 16px',
          fontSize: '0.875rem',
        },
        sizeSmall: {
          padding: '6px 12px',
          fontSize: '0.8rem',
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          padding: 8,
        },
        sizeSmall: {
          padding: 4,
        },
      },
      defaultProps: {
        size: 'small',
      },
    },
    MuiSvgIcon: {
      defaultProps: {
        fontSize: 'small',
      },
      styleOverrides: {
        fontSizeSmall: {
          fontSize: '1.25rem',
        },
      },
    },
    MuiToolbar: {
      styleOverrides: {
        dense: {
          minHeight: 48,
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        dense: {
          paddingTop: 4,
          paddingBottom: 4,
        },
      },
    },
    MuiCardHeader: {
      styleOverrides: {
        root: {
          padding: '12px 16px',
        },
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          padding: '12px 16px',
          '&:last-child': {
            paddingBottom: '12px',
          },
        },
      },
    },
  },
}); 