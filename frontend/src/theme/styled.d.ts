import '@mui/material/styles';

declare module 'styled-components' {
  export interface DefaultTheme {
    zIndex: {
      drawer: number;
      appBar: number;
      modal: number;
      snackbar: number;
      tooltip: number;
    };
    palette: {
      background: {
        default: string;
        paper: string;
      };
      divider: string;
    };
  }
} 