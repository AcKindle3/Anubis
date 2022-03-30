import React, {useState} from 'react';
import {ThemeProvider} from '@material-ui/core/styles';
import theme from './theme/Theme';

import Root from './Root';

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <Root />
    </ThemeProvider>
  );
}
