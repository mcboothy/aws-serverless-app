import React from 'react'
import Stack from '@mui/material/Stack';
import MainMenu from './components/MainMenu'
import Map from './components/Map'
import Navigator from './components/Navigator';
import Box from '@mui/material/Box'
//import Grid from '@mui/material/Grid'; // Grid version 1
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

const App = () => {

  return (
    <React.Fragment>
      <Grid container>
        <Grid xs={12}>
          <MainMenu />
        </Grid>
        <Grid xs={3}>
          <Navigator />
        </Grid>
        <Grid xs={9}>
          <Map />
        </Grid>
      </Grid >
    </React.Fragment>
  );
}

export default App;
