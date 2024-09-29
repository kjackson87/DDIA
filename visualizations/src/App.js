import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import LinearizabilityViz from './visualizations/LinearizabilityViz';
import CausalOrderViz from './visualizations/CausalOrderViz';
import LockingViz from './visualizations/LockingViz';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Distributed Systems Visualizations</h1>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/linearizability" element={<LinearizabilityViz />} />
          <Route path="/causal-order" element={<CausalOrderViz />} />
          <Route path="/locking" element={<LockingViz />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="home-container">
      <h2>Welcome to Distributed Systems Visualizations</h2>
      <nav>
        <ul className="visualization-list">
          <li>
            <Link to="/linearizability" className="viz-link">
              <span className="viz-title">Linearizability Visualization</span>
              <span className="viz-description">Explore the concept of linearizability in distributed systems</span>
            </Link>
          </li>
          <li>
            <Link to="/causal-order" className="viz-link">
              <span className="viz-title">Causal Order Visualization</span>
              <span className="viz-description">Understand the causal order in distributed systems</span>
            </Link>
          </li>
          <li>
            <Link to="/locking" className="viz-link">
              <span className="viz-title">Locking Visualization</span>
              <span className="viz-description">Explore the concept of locking in distributed systems</span>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}

export default App;