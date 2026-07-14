import React, { useEffect, useState } from 'react';
import '../styles/Dashboard.css';

interface Stats {
  total_alerts: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  new_count: number;
  acknowledged_count: number;
  resolved_count: number;
  escalated_count: number;
  average_resolution_time?: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/v1/alerts/stats/summary?time_period=24h');
        if (!response.ok) throw new Error('Failed to fetch stats');
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="dashboard-error">Error: {error}</div>;
  }

  return (
    <div className="dashboard">
      <h2>Alert Dashboard</h2>
      {stats && (
        <div className="dashboard-grid">
          <div className="stat-card critical">
            <h3>Critical</h3>
            <p className="stat-value">{stats.critical_count}</p>
          </div>
          <div className="stat-card high">
            <h3>High</h3>
            <p className="stat-value">{stats.high_count}</p>
          </div>
          <div className="stat-card medium">
            <h3>Medium</h3>
            <p className="stat-value">{stats.medium_count}</p>
          </div>
          <div className="stat-card low">
            <h3>Low</h3>
            <p className="stat-value">{stats.low_count}</p>
          </div>
          <div className="stat-card">
            <h3>Total Alerts (24h)</h3>
            <p className="stat-value">{stats.total_alerts}</p>
          </div>
          <div className="stat-card">
            <h3>Resolved</h3>
            <p className="stat-value">{stats.resolved_count}</p>
          </div>
          <div className="stat-card">
            <h3>Escalated</h3>
            <p className="stat-value">{stats.escalated_count}</p>
          </div>
          <div className="stat-card">
            <h3>New</h3>
            <p className="stat-value">{stats.new_count}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;