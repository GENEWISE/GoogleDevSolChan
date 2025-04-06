import React from 'react';
import { Brain } from 'lucide-react';
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Requests from './pages/Requests.jsx';
import Chatbot from './pages/Chatbot.jsx';
import About from './pages/About.jsx';
import Home from './pages/Home.jsx';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <div className="nav-container">
            <div className="nav-content">
              <div className="nav-brand">
                <Brain size={32} color="#1a56db" />
                <span>GENE WISE</span>
              </div>
              <div className="nav-links">
                <Link to="/">Home</Link>
                <Link to="/Requests">Requests</Link>
                <Link to="/Chatbot">Chat Bot</Link>
                <Link to="/About">About Us</Link>
              </div>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} /> 
          <Route path="/Requests" element={<Requests />} />
          <Route path="/Chatbot" element={<Chatbot />} />
          <Route path="/About" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
