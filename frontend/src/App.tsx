import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/App.css';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import AlertsList from './pages/AlertsList';
import AlertDetail from './pages/AlertDetail';

function App() {
  const [loading, setLoading] = useState(true);
  const [appReady, setAppReady] = useState(false);

  useEffect(() => {
    // Check API health
    const checkHealth = async () => {
      try {
        const response = await fetch('/api/v1/health');
        if (response.ok) {
          setAppReady(true);
        }
      } catch (error) {
        console.error('Failed to connect to API:', error);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!appReady) {
    return (
      <div className="error-container">
        <h1>Connection Error</h1>
        <p>Unable to connect to the API. Please ensure the backend is running.</p>
      </div>
    );
  }

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/alerts" element={<AlertsList />} />
          <Route path="/alerts/:id" element={<AlertDetail />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;