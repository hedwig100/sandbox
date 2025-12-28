import { Routes, Route } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import Home from './pages/Home';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </div>
  );
}

export default App;
