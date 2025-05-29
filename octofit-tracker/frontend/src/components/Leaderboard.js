import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

// Codespace Django REST API endpoint: https://example-codespace-name-8000.app.github.dev/api/

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true);
        const data = await apiService.getLeaderboard();
        setLeaderboard(data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching leaderboard: ' + err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="d-flex justify-content-center align-items-center" style={{minHeight: '200px'}}>
          <div className="spinner-border loading-spinner" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span className="ms-3">Loading leaderboard...</span>
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

  const sortedLeaderboard = leaderboard.sort((a, b) => b.score - a.score);

  const getRankBadge = (rank) => {
    if (rank === 1) return 'bg-warning text-dark';
    if (rank === 2) return 'bg-secondary';
    if (rank === 3) return 'bg-info';
    return 'bg-light text-dark';
  };

  const getRankIcon = (rank) => {
    if (rank === 1) return 'bi-trophy-fill';
    if (rank === 2) return 'bi-award-fill';
    if (rank === 3) return 'bi-star-fill';
    return 'bi-hash';
  };

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4 text-center">
            <i className="bi bi-trophy me-2"></i>
            Leaderboard
          </h1>
          {sortedLeaderboard.length === 0 ? (
            <div className="alert alert-info text-center">
              <i className="bi bi-info-circle me-2"></i>
              No leaderboard entries found
            </div>
          ) : (
            <div className="card">
              <div className="card-header">
                <h5 className="mb-0">
                  <i className="bi bi-list-ol me-2"></i>
                  Top Performers ({sortedLeaderboard.length} participants)
                </h5>
              </div>
              <div className="card-body p-0">
                <div className="table-responsive">
                  <table className="table table-striped table-hover mb-0">
                    <thead>
                      <tr>
                        <th scope="col" style={{width: '80px'}}>
                          <i className="bi bi-hash me-2"></i>
                          Rank
                        </th>
                        <th scope="col">
                          <i className="bi bi-person me-2"></i>
                          Username
                        </th>
                        <th scope="col" style={{width: '120px'}}>
                          <i className="bi bi-star me-2"></i>
                          Score
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {sortedLeaderboard.map((entry, index) => {
                        const rank = index + 1;
                        return (
                          <tr key={entry.id} className={rank <= 3 ? 'table-warning' : ''}>
                            <td>
                              <span className={`badge ${getRankBadge(rank)} d-flex align-items-center justify-content-center`} style={{width: '40px', height: '40px'}}>
                                <i className={`bi ${getRankIcon(rank)} me-1`}></i>
                                {rank}
                              </span>
                            </td>
                            <td>
                              <strong className={rank <= 3 ? 'text-primary' : ''}>
                                {entry.user.username || 'Unknown'}
                              </strong>
                              {rank === 1 && <span className="badge bg-warning text-dark ms-2">Champion</span>}
                              {rank === 2 && <span className="badge bg-secondary ms-2">Runner-up</span>}
                              {rank === 3 && <span className="badge bg-info ms-2">Third Place</span>}
                            </td>
                            <td>
                              <span className="badge bg-success fs-6">
                                {entry.score} pts
                              </span>
                            </td>
                          </tr>
                        );
                      })}
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

export default Leaderboard;