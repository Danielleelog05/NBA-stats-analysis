import React from 'react';
import { motion } from 'framer-motion';
import './About.css';

const About = () => {
  const projectInfo = {
    name: 'NBA Stats Analysis',
    version: '1.0.0',
    description: 'Advanced basketball analytics platform that transforms basic NBA statistics into comprehensive player performance insights through higher-order metrics and interactive visualizations.',
    features: [
      'Automated data collection from multiple NBA sources',
      'Higher-order statistics calculation',
      'Player strength evaluation model',
      'Interactive visualizations and dashboards',
      'Real-time data processing and analysis'
    ],
    technologies: [
      'Python (Pandas, NumPy, Scikit-learn)',
      'React.js (Frontend)',
      'BeautifulSoup4 (Web Scraping)',
      'Plotly & D3.js (Visualizations)',
      'Streamlit (Dashboard)'
    ],
    dataSources: [
      'Basketball Reference',
      'NBA.com Official Statistics',
      'Kaggle Basketball Datasets'
    ]
  };

  const teamInfo = [
    {
      name: 'Data Collection Team',
      role: 'Web Scraping & Data Pipeline',
      description: 'Responsible for automated data collection from multiple NBA sources, ensuring data quality and reliability.',
      skills: ['Python', 'BeautifulSoup4', 'Selenium', 'Data Cleaning']
    },
    {
      name: 'Analytics Team',
      role: 'Statistical Analysis & Modeling',
      description: 'Develops higher-order statistics and player evaluation models using advanced analytics techniques.',
      skills: ['Statistics', 'Machine Learning', 'Python', 'Pandas']
    },
    {
      name: 'Visualization Team',
      role: 'Interactive Dashboards & Charts',
      description: 'Creates compelling visualizations and interactive dashboards for data exploration and insights.',
      skills: ['D3.js', 'Plotly', 'React', 'Data Visualization']
    },
    {
      name: 'Web Development Team',
      role: 'Frontend & User Experience',
      description: 'Builds the web application interface and ensures optimal user experience across all devices.',
      skills: ['React.js', 'JavaScript', 'CSS', 'UX Design']
    }
  ];

  return (
    <div className="about">
      <div className="container">
        {/* Header Section */}
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1>About NBA Stats Analysis</h1>
          <p>Advanced basketball analytics platform for comprehensive player performance analysis</p>
        </motion.div>

        {/* Project Overview */}
        <motion.section
          className="project-overview"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="overview-card">
            <h2>Project Overview</h2>
            <p>{projectInfo.description}</p>

            <div className="project-meta">
              <div className="meta-item">
                <strong>Version:</strong> {projectInfo.version}
              </div>
              <div className="meta-item">
                <strong>Status:</strong> Active Development
              </div>
              <div className="meta-item">
                <strong>License:</strong> MIT
              </div>
            </div>
          </div>
        </motion.section>

        {/* Key Features */}
        <motion.section
          className="key-features"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <h2>Key Features</h2>
          <div className="features-grid">
            {projectInfo.features.map((feature, index) => (
              <motion.div
                key={index}
                className="feature-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
              >
                <i className="fas fa-check-circle"></i>
                <span>{feature}</span>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Technology Stack */}
        <motion.section
          className="technology-stack"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h2>Technology Stack</h2>
          <div className="tech-grid">
            {projectInfo.technologies.map((tech, index) => (
              <motion.div
                key={index}
                className="tech-item"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.8 + index * 0.1 }}
              >
                <span>{tech}</span>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Data Sources */}
        <motion.section
          className="data-sources"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <h2>Data Sources</h2>
          <p>Our platform aggregates data from multiple reliable NBA statistics sources:</p>
          <div className="sources-list">
            {projectInfo.dataSources.map((source, index) => (
              <motion.div
                key={index}
                className="source-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 1.0 + index * 0.1 }}
              >
                <i className="fas fa-database"></i>
                <span>{source}</span>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Team Information */}
        <motion.section
          className="team-info"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
        >
          <h2>Development Team</h2>
          <div className="team-grid">
            {teamInfo.map((team, index) => (
              <motion.div
                key={index}
                className="team-card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 1.2 + index * 0.1 }}
              >
                <div className="team-header">
                  <h3>{team.name}</h3>
                  <span className="role">{team.role}</span>
                </div>
                <p className="description">{team.description}</p>
                <div className="skills">
                  <h4>Skills:</h4>
                  <div className="skills-list">
                    {team.skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Contact Information */}
        <motion.section
          className="contact-info"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.4 }}
        >
          <div className="contact-card">
            <h2>Get in Touch</h2>
            <p>Have questions or want to contribute to the project?</p>
            <div className="contact-links">
              <a href="mailto:contact@nba-stats-analysis.com" className="contact-link">
                <i className="fas fa-envelope"></i>
                Email Us
              </a>
              <a href="#" className="contact-link">
                <i className="fab fa-github"></i>
                GitHub Repository
              </a>
              <a href="#" className="contact-link">
                <i className="fas fa-book"></i>
                Documentation
              </a>
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  );
};

export default About;