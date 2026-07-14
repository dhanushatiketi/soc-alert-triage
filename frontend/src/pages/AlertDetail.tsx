import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/AlertDetail.css';

interface Alert {
  id: number;
  title: string;
  description: string;
  source: string;
  severity: string;
  category: string;
  status: string;
  created_at: string;
  updated_at: string;
  detected_at: string;
  resolved_at?: string;
  is_acknowledged: boolean;
  is_escalated: boolean;
  assigned_to?: string;
  assigned_team?: string;
  ticket_id?: string;
  metadata?: Record<string, any>;
}

const AlertDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [alert, setAlert] = useState<Alert | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAlert = async () => {
      try {
        const response = await fetch(`/api/v1/alerts/${id}`);
        if (!response.ok) throw new Error('Failed to fetch alert');
        const data = await response.json();
        setAlert(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchAlert();
    }
  }, [id]);

  const handleAcknowledge = async () => {
    try {
      const response = await fetch(`/api/v1/alerts/${id}/acknowledge`, {
        method: 'POST',
      });
      if (response.ok) {
        const data = await response.json();
        setAlert(data);
      }
    } catch (err) {
      console.error('Failed to acknowledge alert:', err);
    }
  };

  const handleEscalate = async () => {
    try {
      const response = await fetch(`/api/v1/alerts/${id}/escalate`, {
        method: 'POST',
      });
      if (response.ok) {
        const data = await response.json();
        setAlert(data);
      }
    } catch (err) {
      console.error('Failed to escalate alert:', err);
    }
  };

  const handleResolve = async () => {
    try {
      const response = await fetch(`/api/v1/alerts/${id}/resolve`, {
        method: 'POST',
      });
      if (response.ok) {
        const data = await response.json();
        setAlert(data);
      }
    } catch (err) {
      console.error('Failed to resolve alert:', err);
    }
  };

  if (loading) {
    return <div className="detail-loading">Loading alert...</div>;
  }

  if (error) {
    return <div className="detail-error">Error: {error}</div>;
  }

  if (!alert) {
    return <div className="detail-error">Alert not found</div>;
  }

  return (
    <div className="alert-detail">
      <button onClick={() => navigate('/alerts')} className="back-button">
        ← Back to Alerts
      </button>

      <div className="alert-header">
        <h2>{alert.title}</h2>
        <div className="alert-metadata">
          <span className={`severity-badge severity-${alert.severity.toLowerCase()}`}>
            {alert.severity}
          </span>
          <span className="status-badge">{alert.status}</span>
        </div>
      </div>

      <div className="alert-content">
        <div className="section">
          <h3>Details</h3>
          <div className="details-grid">
            <div>
              <strong>Source:</strong>
              <p>{alert.source}</p>
            </div>
            <div>
              <strong>Category:</strong>
              <p>{alert.category || 'N/A'}</p>
            </div>
            <div>
              <strong>Created:</strong>
              <p>{new Date(alert.created_at).toLocaleString()}</p>
            </div>
            <div>
              <strong>Updated:</strong>
              <p>{new Date(alert.updated_at).toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="section">
          <h3>Description</h3>
          <p>{alert.description || 'No description provided'}</p>
        </div>

        <div className="section">
          <h3>Actions</h3>
          <div className="action-buttons">
            {!alert.is_acknowledged && (
              <button onClick={handleAcknowledge} className="btn btn-primary">
                Acknowledge
              </button>
            )}
            {!alert.is_escalated && (
              <button onClick={handleEscalate} className="btn btn-warning">
                Escalate
              </button>
            )}
            {alert.status !== 'resolved' && (
              <button onClick={handleResolve} className="btn btn-success">
                Resolve
              </button>
            )}
          </div>
        </div>

        {alert.metadata && Object.keys(alert.metadata).length > 0 && (
          <div className="section">
            <h3>Metadata</h3>
            <pre className="metadata">{JSON.stringify(alert.metadata, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default AlertDetail;