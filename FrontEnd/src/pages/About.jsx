import React from 'react';
import { Users, Brain, Globe, Award } from 'lucide-react';

function About() {
  return (
    <div className="about-page">
      <div className="page-container">
        <div className="page-header">
          <Users size={48} color="#1a56db" />
          <h1>About Gene Wise</h1>
          <p>Advancing the future of genetic research through artificial intelligence</p>
        </div>

        <div className="about-content">
          <div className="about-section">
            <div className="section-icon">
              <Brain size={32} color="#1a56db" />
            </div>
            <h2>Our Mission</h2>
            <p>
              Gene Wise is dedicated to revolutionizing genetic research through
              the integration of cutting-edge AI technology. We aim to accelerate
              scientific discoveries and improve human health understanding.
            </p>
          </div>

          <div className="about-section">
            <div className="section-icon">
              <Globe size={32} color="#1a56db" />
            </div>
            <h2>Global Impact</h2>
            <p>
              Our platform connects researchers worldwide, facilitating
              collaboration and knowledge sharing across the global scientific
              community. We believe in the power of collective intelligence.
            </p>
          </div>

          <div className="about-section">
            <div className="section-icon">
              <Award size={32} color="#1a56db" />
            </div>
            <h2>Innovation & Excellence</h2>
            <p>
              Through continuous innovation and rigorous scientific standards,
              we're pushing the boundaries of what's possible in genetic research
              and analysis.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About;