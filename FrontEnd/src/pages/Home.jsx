import React from "react";
import { LineChart, MessageSquare, Users, Heart, Stethoscope, Clock, Phone, Calendar, Mail, MapPin } from 'lucide-react';

const Home = () => {
  return (
    <div>
      <section className="hero">
        <div className="hero-container">
          <div className="hero-content">
            <div className="hero-text">
              <h1 className="hero-title">Advancing Genetic Research Through AI</h1>
            </div>
            <div className="hero-image">
              <div className="hero-features">
                <p className="hero-feature">
                  Advanced gene analysis and prediction Lorem ipsum dolor sit amet consectetur adipisicing elit.
                </p>
              </div>
              <img
                src="https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&q=80"
                alt="Gene Research"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="features">
        <div className="features-container">
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <LineChart size={48} color="#1a56db" />
              </div>
              <h3 className="feature-title">Predictive Analysis</h3>
              <p className="feature-description">Advanced AI-driven genetic prediction models</p>
            </div>
            <div className="feature-card highlighted">
              <div className="feature-icon">
                <MessageSquare size={48} color="white" />
              </div>
              <h3 className="feature-title">Expert Chat</h3>
              <p className="feature-description">24/7 access to AI-powered genetic consultation</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <Users size={48} color="#1a56db" />
              </div>
              <h3 className="feature-title">Collaboration</h3>
              <p className="feature-description">Connect with leading genetic researchers</p>
            </div>
          </div>
        </div>
      </section>
      <section className="content">
        <div className="content-grid">
          <div className="content-card">
            <h3 className="content-title">Prediction</h3>
            <p className="content-description">
              Leading the way in genetic research with breakthrough discoveries and innovative methodologies.
            </p>
          </div>
          <div className="content-card">
            <h3 className="content-title">Chat Bot</h3>
            <p className="content-description">
              Connected with research institutions worldwide, sharing knowledge and resources.
            </p>
          </div>
          <div className="content-card">
            <h3 className="content-title">Upload File</h3>
            <p className="content-description">
              Leveraging cutting-edge AI technology to advance genetic research capabilities.
            </p>
          </div>
          <div className="content-card">
            <h3 className="content-title">Submit</h3>
            <p className="content-description">
              Committed to shaping the future of genetic research and personalized medicine.
            </p>
          </div>
        </div>
      </section>
      <footer className="footer">
        <div className="footer-container">
          <div className="footer-section">
            <h3>About Us</h3>
            <p>GeneWise is dedicated to providing exceptional healthcare services with a focus on patient comfort and recovery.</p>
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul className="footer-links">
              <li><a href="#">Services</a></li>
              <li><a href="#">Doctors</a></li>
              <li><a href="#">Appointments</a></li>
              <li><a href="#">Emergency</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h3>Contact Info</h3>
            <ul className="footer-links">
              <li>
                <Phone className="h-4 w-4" style={{ display: 'inline', marginRight: '8px' }} />
                1-800-000000000
              </li>
              <li>
                <Mail className="h-4 w-4" style={{ display: 'inline', marginRight: '8px' }} />
                info@genewise.com
              </li>
              <li>
                <MapPin className="h-4 w-4" style={{ display: 'inline', marginRight: '8px' }} />
                123 Healthcare Ave, Medical City
              </li>
            </ul>
          </div>
        </div>
        <div className="footer-container footer-bottom">
          <p>&copy; 2025 GeneWise. All rights reserved.</p>
        </div>
      </footer> 
    </div>
  );
};

export default Home;
