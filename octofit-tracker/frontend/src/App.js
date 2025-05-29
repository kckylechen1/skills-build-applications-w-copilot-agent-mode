import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Import components
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  const WelcomeHome = () => (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <div className="jumbotron bg-primary text-white rounded p-5 text-center mb-4">
            <h1 className="display-4 mb-3">
              <i className="bi bi-heart-pulse me-3"></i>
              Welcome to OctoFit Tracker
            </h1>
            <p className="lead mb-4">
              Track your fitness journey with Mergington High School's premier fitness tracking application
            </p>
            <hr className="my-4" style={{borderColor: 'rgba(255,255,255,0.3)'}} />
            <p className="mb-4">
              Monitor activities, compete on leaderboards, join teams, and discover new workouts!
            </p>
            <div className="row mt-4">
              <div className="col-md-3 col-6 mb-3">
                <Link to="/activities" className="btn btn-outline-light btn-lg w-100">
                  <i className="bi bi-activity d-block mb-2" style={{fontSize: '2rem'}}></i>
                  Activities
                </Link>
              </div>
              <div className="col-md-3 col-6 mb-3">
                <Link to="/leaderboard" className="btn btn-outline-light btn-lg w-100">
                  <i className="bi bi-trophy d-block mb-2" style={{fontSize: '2rem'}}></i>
                  Leaderboard
                </Link>
              </div>
              <div className="col-md-3 col-6 mb-3">
                <Link to="/teams" className="btn btn-outline-light btn-lg w-100">
                  <i className="bi bi-people d-block mb-2" style={{fontSize: '2rem'}}></i>
                  Teams
                </Link>
              </div>
              <div className="col-md-3 col-6 mb-3">
                <Link to="/workouts" className="btn btn-outline-light btn-lg w-100">
                  <i className="bi bi-lightning d-block mb-2" style={{fontSize: '2rem'}}></i>
                  Workouts
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <Router>
      <div className="App">
        <header className="App-header py-3">
          <div className="container">
            <div className="row align-items-center">
              <div className="col-md-6 d-flex align-items-center">
                <div className="logo-container me-3">
                  <img src="/octofitapp-small.png" alt="OctoFit Logo" className="App-logo" />
                </div>
                <div>
                  <h1 className="mb-0">
                    <i className="bi bi-octagon me-2"></i>
                    OctoFit Tracker
                  </h1>
                  <small className="text-muted">Mergington High School Fitness</small>
                </div>
              </div>
              <div className="col-md-6 text-md-end">
                <span className="badge bg-success fs-6">
                  <i className="bi bi-check-circle me-1"></i>
                  System Online
                </span>
              </div>
            </div>
          </div>
        </header>
        
        <nav className="navbar navbar-expand-lg navbar-primary">
          <div className="container">
            <Link className="navbar-brand fw-bold" to="/">
              <i className="bi bi-house-heart me-2"></i>
              OctoFit
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">
                    <i className="bi bi-activity me-1"></i>
                    Activities
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">
                    <i className="bi bi-trophy me-1"></i>
                    Leaderboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">
                    <i className="bi bi-people me-1"></i>
                    Teams
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">
                    <i className="bi bi-person-lines-fill me-1"></i>
                    Users
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">
                    <i className="bi bi-lightning me-1"></i>
                    Workouts
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        
        <main className="min-vh-100">
          <Routes>
            <Route path="/" element={<WelcomeHome />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/users" element={<Users />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </main>
        
        <footer className="App-footer py-4">
          <div className="container">
            <div className="row align-items-center">
              <div className="col-md-6">
                <h6 className="mb-1">
                  <i className="bi bi-heart-pulse me-2"></i>
                  OctoFit Tracker
                </h6>
                <p className="mb-0 text-muted">
                  Empowering Mergington High School's fitness journey
                </p>
              </div>
              <div className="col-md-6 text-md-end">
                <p className="mb-1">
                  <a
                    className="App-link text-decoration-none"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <i className="bi bi-code-slash me-1"></i>
                    Built with React
                  </a>
                </p>
                <small className="text-muted">
                  © 2024 Mergington High School
                </small>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
