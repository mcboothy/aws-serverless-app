import * as React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import DialogContentText from '@mui/material/DialogContentText';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import axios from 'axios';

const navItems = ['Home', 'About', 'Contact'];

function MainMenu(props) {
  const [open, setOpen] = React.useState(false);
  const [content, setContent] = React.useState('');

  const openDialog = () => {
    axios.post(`/prod/endpoint1`, { name: 'hello from react' })
    .then((res) => {
      console.log(res.data);
      setContent(`Content changed\nData = ${res.data.message}`)
      setOpen(true);
    })
    .catch(function (error) {
      setContent(`Error calling ${window.BASE_URL}/endpoint1`);
      console.log(error);
      setOpen(true);
    });  
  };

  const closeDialog = () => {
    setOpen(false);
  };

  return (
    <React.Fragment>
      <AppBar component='nav' style={{position: 'relative'}}>
        <Toolbar>
          <IconButton size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Russ Test
          </Typography>
          <Button color="inherit" onClick={openDialog}>
            Test
          </Button>
        </Toolbar>
      </AppBar>      
      <Dialog
        open={open}
        onClose={closeDialog}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Worked !!!"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {content}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeDialog}>OK</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}

export default MainMenu;