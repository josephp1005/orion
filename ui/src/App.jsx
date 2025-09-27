import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import WelcomePage from './pages/WelcomePage';
import DocPage from './pages/DocPage';
import AskPage from './pages/AskPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<WelcomePage />} />
          <Route path="docs/:collection/:slug" element={<DocPage />} />
          <Route path="ask" element={<AskPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
