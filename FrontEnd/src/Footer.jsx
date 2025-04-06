import { Heart, Stethoscope, Clock, Phone, Calendar, Users, Mail, MapPin } from 'lucide-react';
import React from 'react';

function Footer(){
    return(
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
    );
}

export default Footer;