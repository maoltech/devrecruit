import * as React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container } from '@mui/material';
import Dashboard from './pages/Dashboard';
import TransactionHistory from './pages/TransactionHistory';

const App: React.FC = () => {
  return (
    <Router>
      <Container maxWidth="lg">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/transactions" element={<TransactionHistory />} />
        </Routes>
      </Container>
    </Router>
  );
};

export default App;