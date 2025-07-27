import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>NBA Stats Analysis</h3>
            <p>Advanced basketball analytics and player performance insights</p>
            <div className="social-links">
              <a href="#" aria-label="GitHub">
                <i className="fab fa-github"></i>
              </a>
              <a href="#" aria-label="Twitter">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="#" aria-label="LinkedIn">
                <i className="fab fa-linkedin"></i>
              </a>
            </div>
          </div>

          <div className="footer-section">
            <h4>Features</h4>
            <ul>
              <li><Link to="/dashboard">Interactive Dashboard</Link></li>
              <li><Link to="/player-analysis">Player Analysis</Link></li>
              <li><Link to="/data-collection">Data Collection</Link></li>
              <li><Link to="/about">About Project</Link></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Data Sources</h4>
            <ul>
              <li><a href="https://www.basketball-reference.com" target="_blank" rel="noopener noreferrer">Basketball Reference</a></li>
              <li><a href="https://www.nba.com/stats" target="_blank" rel="noopener noreferrer">NBA.com Stats</a></li>
              <li><a href="https://www.kaggle.com/datasets" target="_blank" rel="noopener noreferrer">Kaggle Datasets</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Contact</h4>
            <ul>
              <li><a href="mailto:contact@nba-stats-analysis.com">Email Us</a></li>
              <li><a href="#" target="_blank" rel="noopener noreferrer">Documentation</a></li>
              <li><a href="#" target="_blank" rel="noopener noreferrer">API Reference</a></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {currentYear} NBA Stats Analysis. All rights reserved.</p>
          <div className="footer-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Cookie Policy</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;