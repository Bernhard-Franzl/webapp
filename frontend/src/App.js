import { Theme } from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { Route, Routes } from 'react-router-dom';
//import Topbar from './scenes/global/Topbar';
import FancySidebar from './scenes/global/Sidebar';
import Dashboard from './scenes/dashboard';
import LectureHall18 from './scenes/lh18';
import LectureHall19 from './scenes/lh19';


function App() {
  const theme = Theme;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">

        <FancySidebar />

        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/lh18" element={<LectureHall18 />} />
            <Route path="/lh19" element={<LectureHall19 />} />
          </Routes>
        </main>
        
      </div>
    </ThemeProvider>
  );
}

export default App;
