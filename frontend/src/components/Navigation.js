import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';

function Navigation() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
          }}
        >
          Case Management System
        </Typography>
        <Box>
          <Button color="inherit" component={RouterLink} to="/">
            Dashboard
          </Button>
          <Button color="inherit" component={RouterLink} to="/cases">
            Cases
          </Button>
          <Button color="inherit" component={RouterLink} to="/predictions">
            Predictions
          </Button>
          <Button color="inherit" component={RouterLink} to="/insights">
            Insights
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navigation; 