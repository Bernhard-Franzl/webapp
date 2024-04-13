import {Box, IconButton, useTheme} from '@mui/material';
import { useContext } from 'react';
import { Theme, tokens } from '../../theme';
import InputBase from '@mui/material';
// snack nice icons from mui

const Topbar = () => {
  // grabs theme from the theme provider
  const theme = useTheme();
  const colors = tokens(theme.palette)

  return <Box display="flex" justifyContent="space-between" p={2}>
    <Box>Home</Box>
    <Box>HS18</Box>
    <Box>HS19</Box>
  </Box>;
}

export default Topbar;  