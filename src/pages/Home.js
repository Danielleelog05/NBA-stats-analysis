import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import axios from 'axios';
import './Home.css';

const Home = () => {
  // Mock data for demonstration - in real app, this would come from your backend
  const { data: stats, isLoading } = useQuery('homeStats', async () => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      totalPlayers: 450,
      seasonsAnalyzed: 5,
      dataPoints: 25000,
      lastUpdated: new Date().toLocaleDateString()
    };
  });

  const features = [
    {
      icon: 'fas fa-chart-line',
      title: 'Advanced Analytics',
      description: 'Higher-order statistics and advanced metrics beyond traditional box scores',
      color: '#3b82f6'
    },
    {
      icon: 'fas fa-user-friends',
      title: 'Player Analysis',
      description: 'Comprehensive player strength evaluation and performance insights',
      color: '#10b981'
    },
    {
      icon: 'fas fa-database',
      title: 'Data Collection',
      description: 'Automated web scraping from multiple NBA data sources',
      color: '#f59e0b'
    },
    {
      icon: 'fas fa-chart-bar',
      title: 'Interactive Visualizations',
      description: 'Dynamic charts and dashboards for data exploration',
      color: '#ef4444'
    }
  ];

  const dataSources = [
    {
      name: 'Basketball Reference',
      url: 'https://www.basketball-reference.com',
      description: 'Comprehensive NBA statistics and historical data'
    },
    {
      name: 'NBA.com Stats',
      url: 'https://www.nba.com/stats',
      description: 'Official NBA statistics and advanced metrics'
    },
    {
      name: 'Kaggle Datasets',
      url: 'https://www.kaggle.com/datasets',
      description: 'Curated basketball datasets for analysis'
    }
  ];

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <motion.div
            className="hero-content"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="hero-title">
              NBA Stats Analysis
              <span className="hero-subtitle">Beyond the Box Score</span>
            </h1>
            <p className="hero-description">
              Advanced basketball analytics platform that transforms basic NBA statistics
              into comprehensive player performance insights through higher-order metrics
              and interactive visualizations.
            </p>
            <div className="hero-actions">
              <Link to="/dashboard" className="btn btn-primary">
                <i className="fas fa-chart-line"></i>
                Explore Dashboard
              </Link>
              <Link to="/player-analysis" className="btn btn-secondary">
                <i className="fas fa-user-friends"></i>
                Player Analysis
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Overview */}
      {!isLoading && stats && (
        <section className="stats-overview">
          <div className="container">
            <motion.div
              className="stats-grid"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <div className="stat-card">
                <i className="fas fa-users"></i>
                <h3>{stats.totalPlayers.toLocaleString()}</h3>
                <p>Players Analyzed</p>
              </div>
              <div className="stat-card">
                <i className="fas fa-calendar-alt"></i>
                <h3>{stats.seasonsAnalyzed}</h3>
                <p>Seasons Analyzed</p>
              </div>
              <div className="stat-card">
                <i className="fas fa-database"></i>
                <h3>{stats.dataPoints.toLocaleString()}</h3>
                <p>Data Points</p>
              </div>
              <div className="stat-card">
                <i className="fas fa-clock"></i>
                <h3>{stats.lastUpdated}</h3>
                <p>Last Updated</p>
              </div>
            </motion.div>
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <motion.div
            className="section-header"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2>Key Features</h2>
            <p>Comprehensive tools for NBA analytics and player evaluation</p>
          </motion.div>

          <div className="features-grid">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                className="feature-card"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="feature-icon" style={{ backgroundColor: feature.color }}>
                  <i className={feature.icon}></i>
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Data Sources Section */}
      <section className="data-sources">
        <div className="container">
          <motion.div
            className="section-header"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2>Data Sources</h2>
            <p>Reliable and comprehensive NBA data collection from multiple sources</p>
          </motion.div>

          <div className="sources-grid">
            {dataSources.map((source, index) => (
              <motion.div
                key={source.name}
                className="source-card"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <h3>{source.name}</h3>
                <p>{source.description}</p>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="source-link"
                >
                  Visit Source <i className="fas fa-external-link-alt"></i>
                </a>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <motion.div
            className="cta-content"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2>Ready to Explore NBA Analytics?</h2>
            <p>Start analyzing player performance with our advanced tools and insights</p>
            <div className="cta-actions">
              <Link to="/dashboard" className="btn btn-primary">
                <i className="fas fa-rocket"></i>
                Get Started
              </Link>
              <Link to="/about" className="btn btn-secondary">
                <i className="fas fa-info-circle"></i>
                Learn More
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;