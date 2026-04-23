import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Oceanographic from './pages/Oceanographic';
import Fisheries from './pages/Fisheries';
import Taxonomy from './pages/Taxonomy';
import Molecular from './pages/Molecular';
import Analytics from './pages/Analytics';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/oceanographic" element={<Oceanographic />} />
          <Route path="/fisheries" element={<Fisheries />} />
          <Route path="/taxonomy" element={<Taxonomy />} />
          <Route path="/molecular" element={<Molecular />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
