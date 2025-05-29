import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

// Codespace Django REST API endpoint: https://example-codespace-name-8000.app.github.dev/api/

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        setLoading(true);
        const data = await apiService.getTeams();
        setTeams(data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching teams: ' + err.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="d-flex justify-content-center align-items-center" style={{minHeight: '200px'}}>
          <div className="spinner-border loading-spinner" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span className="ms-3">Loading teams...</span>
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
            <i className="bi bi-people me-2"></i>
            Teams
          </h1>
          {teams.length === 0 ? (
            <div className="alert alert-info text-center">
              <i className="bi bi-info-circle me-2"></i>
              No teams found
            </div>
          ) : (
            <>
              <div className="mb-4 text-center">
                <span className="badge bg-primary fs-6">
                  <i className="bi bi-collection me-2"></i>
                  {teams.length} Team{teams.length !== 1 ? 's' : ''} Available
                </span>
              </div>
              <div className="row">
                {teams.map((team) => (
                  <div key={team.id} className="col-md-6 col-lg-4 mb-4">
                    <div className="card h-100 shadow-sm">
                      <div className="card-header bg-primary text-white d-flex align-items-center">
                        <i className="bi bi-shield-check me-2"></i>
                        <h5 className="card-title mb-0">{team.name}</h5>
                      </div>
                      <div className="card-body">
                        <div className="d-flex align-items-center mb-3">
                          <i className="bi bi-people-fill me-2 text-muted"></i>
                          <h6 className="card-subtitle mb-0 text-muted">
                            Team Members ({team.members ? team.members.length : 0})
                          </h6>
                        </div>
                        {team.members && team.members.length > 0 ? (
                          <div className="list-group list-group-flush">
                            {team.members.map((member, index) => (
                              <div key={member.id} className="list-group-item px-0 py-2 border-0">
                                <div className="d-flex align-items-center">
                                  <span className="badge bg-light text-dark me-2">
                                    {index + 1}
                                  </span>
                                  <i className="bi bi-person me-2 text-primary"></i>
                                  <strong>{member.username || 'Unknown'}</strong>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-3">
                            <i className="bi bi-person-x text-muted" style={{fontSize: '2rem'}}></i>
                            <p className="card-text text-muted mt-2 mb-0">
                              No members in this team
                            </p>
                          </div>
                        )}
                      </div>
                      <div className="card-footer bg-light">
                        <small className="text-muted">
                          <i className="bi bi-info-circle me-1"></i>
                          Team ID: {team.id}
                        </small>
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

export default Teams;