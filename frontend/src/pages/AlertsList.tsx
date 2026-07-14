import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/AlertsList.css';

interface Alert {
  id: number;
  title: string;
  source: string;
  severity: string;
  status: string;
  created_at: string;
  is_acknowledged: boolean;
  is_escalated: boolean;
}

const AlertsList: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await fetch('/api/v1/alerts?limit=50');
        if (!response.ok) throw new Error('Failed to fetch alerts');
        const data = await response.json();
        setAlerts(data.items || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []);

  const getSeverityClass = (severity: string) => {
    return `severity-${severity.toLowerCase()}`;
  };

  if (loading) {
    return <div className="alerts-loading">Loading alerts...</div>;
  }

  if (error) {
    return <div className="alerts-error">Error: {error}</div>;
  }

  return (
    <div className="alerts-container">
      <h2>Security Alerts</h2>
      {alerts.length === 0 ? (
        <p className="no-alerts">No alerts found</p>
      ) : (
        <table className="alerts-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Source</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((alert) => (
              <tr key={alert.id} className={getSeverityClass(alert.severity)}>
                <td>
                  <Link to={`/alerts/${alert.id}`}>{alert.title}</Link>
                </td>
                <td>{alert.source}</td>
                <td>
                  <span className={`severity-badge ${getSeverityClass(alert.severity)}`}>
                    {alert.severity}
                  </span>
                </td>
                <td>{alert.status}</td>
                <td>{new Date(alert.created_at).toLocaleString()}</td>
                <td>
                  <Link to={`/alerts/${alert.id}`} className="view-link">
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AlertsList;