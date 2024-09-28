import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import LinearizabilityViz from './LinearizabilityViz';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Distributed Systems Visualizations</h1>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/linearizability" element={<LinearizabilityViz />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <h2>Welcome to Distributed Systems Visualizations</h2>
      <nav>
        <ul>
          <li><Link to="/linearizability">Linearizability Visualization</Link></li>
          {/* Add more links here as you create more visualizations */}
        </ul>
      </nav>
    </div>
  );
}

export default App;