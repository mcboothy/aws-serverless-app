import { red } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';

// A custom theme for this app
const theme = createTheme({
    palette: {
      mode: 'light',
      primary: {
        main: '#0e24c1',
      },
      secondary: {
        main: '#f50057',
      },
    },
  }
);

export default theme;