import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const data = await apiService.getUsers();
        setUsers(data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching users: ' + err.message);
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="d-flex justify-content-center align-items-center" style={{minHeight: '200px'}}>
          <div className="spinner-border loading-spinner" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span className="ms-3">Loading users...</span>
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
            <i className="bi bi-person-lines-fill me-2"></i>
            Users
          </h1>
          {users.length === 0 ? (
            <div className="alert alert-info text-center">
              <i className="bi bi-info-circle me-2"></i>
              No users found
            </div>
          ) : (
            <>
              <div className="mb-4 text-center">
                <span className="badge bg-success fs-6">
                  <i className="bi bi-people me-2"></i>
                  {users.length} Registered User{users.length !== 1 ? 's' : ''}
                </span>
              </div>
              <div className="row">
                {users.map((user, index) => (
                  <div key={user.id} className="col-md-6 col-lg-4 mb-4">
                    <div className="card h-100 shadow-sm">
                      <div className="card-header bg-success text-white d-flex align-items-center">
                        <i className="bi bi-person-circle me-2"></i>
                        <h6 className="mb-0">User #{index + 1}</h6>
                      </div>
                      <div className="card-body">
                        <div className="text-center mb-3">
                          <div className="bg-light rounded-circle d-inline-flex align-items-center justify-content-center" style={{width: '60px', height: '60px'}}>
                            <i className="bi bi-person-fill text-primary" style={{fontSize: '2rem'}}></i>
                          </div>
                        </div>
                        <h5 className="card-title text-center mb-3">
                          <strong>{user.username}</strong>
                        </h5>
                        <div className="d-flex align-items-center mb-2">
                          <i className="bi bi-envelope me-2 text-muted"></i>
                          <small className="text-muted">Email:</small>
                        </div>
                        <p className="card-text">
                          <span className="badge bg-light text-dark w-100 text-start">
                            {user.email}
                          </span>
                        </p>
                      </div>
                      <div className="card-footer bg-light text-center">
                        <small className="text-muted">
                          <i className="bi bi-info-circle me-1"></i>
                          ID: {user.id}
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

export default Users;