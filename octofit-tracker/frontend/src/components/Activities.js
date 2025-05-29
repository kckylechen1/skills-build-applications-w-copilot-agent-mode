import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

// Codespace Django REST API endpoint: https://example-codespace-name-8000.app.github.dev/api/

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        setLoading(true);
        const data = await apiService.getActivities();
        setActivities(data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching activities: ' + err.message);
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="d-flex justify-content-center align-items-center" style={{minHeight: '200px'}}>
          <div className="spinner-border loading-spinner" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span className="ms-3">Loading activities...</span>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="error-message">
          <i className="bi bi-exclamation-triangle me-2"></i>
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4 text-center">Activities</h1>
          {activities.length === 0 ? (
            <div className="alert alert-info text-center">
              <i className="bi bi-info-circle me-2"></i>
              No activities found
            </div>
          ) : (
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">
                  <i className="bi bi-activity me-2"></i>
                  Activity Log ({activities.length} activities)
                </h5>
              </div>
              <div className="card-body p-0">
                <div className="table-responsive">
                  <table className="table table-striped table-hover mb-0">
                    <thead>
                      <tr>
                        <th scope="col">
                          <i className="bi bi-person me-2"></i>
                          User
                        </th>
                        <th scope="col">
                          <i className="bi bi-tag me-2"></i>
                          Activity Type
                        </th>
                        <th scope="col">
                          <i className="bi bi-clock me-2"></i>
                          Duration
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {activities.map((activity) => (
                        <tr key={activity.id}>
                          <td>
                            <strong>{activity.user.username || 'Unknown'}</strong>
                          </td>
                          <td>
                            <span className="badge bg-primary">
                              {activity.activity_type}
                            </span>
                          </td>
                          <td>
                            <span className="text-muted">
                              {activity.duration} minutes
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Activities;