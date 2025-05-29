import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

/**
 * APITest Component
 * 
 * This component demonstrates how to use the API service to fetch data from the backend
 */
const APITest = () => {
  const [apiInfo, setApiInfo] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch API info when component mounts
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get API info
        const info = await apiService.getAPIInfo();
        setApiInfo(info);
        
        // Get users
        const usersData = await apiService.getUsers();
        setUsers(usersData);
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to fetch data. Please try again later.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading API data...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="api-test">
      <h2>API Connection Test</h2>
      
      {apiInfo && (
        <div className="api-info">
          <h3>API Information</h3>
          <p><strong>Message:</strong> {apiInfo.message}</p>
          <p><strong>Version:</strong> {apiInfo.version}</p>
          <p><strong>Local URL:</strong> {apiInfo.local_url}</p>
          <p><strong>Codespace URL:</strong> {apiInfo.codespace_url}</p>
          <p><strong>Codespace Name:</strong> {apiInfo.codespace_name}</p>
        </div>
      )}
      
      <div className="users-list">
        <h3>Users</h3>
        {users.length > 0 ? (
          <ul>
            {users.map(user => (
              <li key={user.id}>{user.username} - {user.email}</li>
            ))}
          </ul>
        ) : (
          <p>No users found.</p>
        )}
      </div>
    </div>
  );
};

export default APITest;