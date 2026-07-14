import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="layout">
      <header className="header">
        <div className="header-content">
          <Link to="/" className="logo">
            <h1>SOC Alert Triage</h1>
          </Link>
          <nav className="nav">
            <Link to="/">Dashboard</Link>
            <Link to="/alerts">Alerts</Link>
          </nav>
        </div>
      </header>
      <main className="main-content">{children}</main>
      <footer className="footer">
        <p>&copy; 2024 SOC Alert Triage System. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;