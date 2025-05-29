import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

// Codespace Django REST API endpoint: https://example-codespace-name-8000.app.github.dev/api/

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        setLoading(true);
        const data = await apiService.getWorkouts();
        setWorkouts(data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching workouts: ' + err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="d-flex justify-content-center align-items-center" style={{minHeight: '200px'}}>
          <div className="spinner-border loading-spinner" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span className="ms-3">Loading workouts...</span>
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
          <h1 className="mb-4 text-center">
            <i className="bi bi-lightning me-2"></i>
            Workouts
          </h1>
          {workouts.length === 0 ? (
            <div className="alert alert-info text-center">
              <i className="bi bi-info-circle me-2"></i>
              No workouts found
            </div>
          ) : (
            <>
              <div className="mb-4 text-center">
                <span className="badge bg-warning text-dark fs-6">
                  <i className="bi bi-collection-play me-2"></i>
                  {workouts.length} Workout{workouts.length !== 1 ? 's' : ''} Available
                </span>
              </div>
              <div className="row">
                {workouts.map((workout, index) => (
                  <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
                    <div className="card h-100 shadow-sm">
                      <div className="card-header bg-warning text-dark d-flex align-items-center">
                        <i className="bi bi-play-circle me-2"></i>
                        <h5 className="card-title mb-0">{workout.name}</h5>
                      </div>
                      <div className="card-body">
                        <div className="text-center mb-3">
                          <div className="bg-light rounded-circle d-inline-flex align-items-center justify-content-center" style={{width: '60px', height: '60px'}}>
                            <i className="bi bi-lightning-fill text-warning" style={{fontSize: '2rem'}}></i>
                          </div>
                        </div>
                        <div className="d-flex align-items-center mb-2">
                          <i className="bi bi-card-text me-2 text-muted"></i>
                          <small className="text-muted">Description:</small>
                        </div>
                        <p className="card-text">
                          {workout.description || 'No description available'}
                        </p>
                      </div>
                      <div className="card-footer bg-light d-flex justify-content-between align-items-center">
                        <small className="text-muted">
                          <i className="bi bi-info-circle me-1"></i>
                          Workout #{index + 1}
                        </small>
                        <button className="btn btn-sm btn-outline-warning">
                          <i className="bi bi-play me-1"></i>
                          Start
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Workouts;