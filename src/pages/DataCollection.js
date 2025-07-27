import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import axios from 'axios';
import toast from 'react-hot-toast';
import './DataCollection.css';

const DataCollection = () => {
  const [isCollecting, setIsCollecting] = useState(false);
  const [selectedSeason, setSelectedSeason] = useState('2024');

  // Mock data for demonstration
  const { data: collectionStats, isLoading } = useQuery('collectionStats', async () => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      lastCollection: '2024-01-15',
      totalPlayers: 450,
      seasonsCollected: 5,
      dataSources: 3,
      collectionTime: '2.5 hours'
    };
  });

  const dataSources = [
    {
      name: 'Basketball Reference',
      url: 'https://www.basketball-reference.com',
      description: 'Comprehensive NBA statistics and historical data',
      status: 'Active',
      lastUpdate: '2024-01-15',
      dataPoints: 'Player stats, team stats, game logs',
      icon: 'fas fa-database',
      color: '#3b82f6'
    },
    {
      name: 'NBA.com Stats',
      url: 'https://www.nba.com/stats',
      description: 'Official NBA statistics and advanced metrics',
      status: 'Active',
      lastUpdate: '2024-01-14',
      dataPoints: 'Advanced stats, player tracking, team analytics',
      icon: 'fas fa-chart-line',
      color: '#10b981'
    },
    {
      name: 'Kaggle Datasets',
      url: 'https://www.kaggle.com/datasets',
      description: 'Curated basketball datasets for analysis',
      status: 'Active',
      lastUpdate: '2024-01-10',
      dataPoints: 'Historical data, player bios, team records',
      icon: 'fas fa-cloud-download-alt',
      color: '#f59e0b'
    }
  ];

  const scrapingFeatures = [
    {
      title: 'Automated Data Collection',
      description: 'Scheduled web scraping from multiple NBA data sources',
      icon: 'fas fa-robot',
      details: [
        'Automated daily/weekly data collection',
        'Error handling and retry mechanisms',
        'Rate limiting to respect server resources',
        'Data validation and cleaning'
      ]
    },
    {
      title: 'Multi-Source Integration',
      description: 'Aggregates data from multiple reliable sources',
      icon: 'fas fa-network-wired',
      details: [
        'Basketball Reference integration',
        'NBA.com official statistics',
        'Kaggle dataset integration',
        'Data source redundancy'
      ]
    },
    {
      title: 'Data Processing Pipeline',
      description: 'Automated cleaning and preprocessing of collected data',
      icon: 'fas fa-cogs',
      details: [
        'Data validation and quality checks',
        'Missing value handling',
        'Data type conversion',
        'Consistent formatting'
      ]
    },
    {
      title: 'Real-time Monitoring',
      description: 'Live monitoring of data collection processes',
      icon: 'fas fa-eye',
      details: [
        'Collection status tracking',
        'Error logging and alerts',
        'Performance metrics',
        'Data freshness monitoring'
      ]
    }
  ];

  const handleStartCollection = async () => {
    setIsCollecting(true);
    toast.loading('Starting data collection...', { id: 'collection' });

    try {
      // Simulate API call to start collection
      await new Promise(resolve => setTimeout(resolve, 3000));

      toast.success('Data collection completed successfully!', { id: 'collection' });
    } catch (error) {
      toast.error('Data collection failed. Please try again.', { id: 'collection' });
    } finally {
      setIsCollecting(false);
    }
  };

  return (
    <div className="data-collection">
      <div className="container">
        {/* Header Section */}
        <motion.div
          className="page-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1>Data Collection</h1>
          <p>Automated web scraping and data collection from multiple NBA sources</p>
        </motion.div>

        {/* Collection Stats */}
        {!isLoading && collectionStats && (
          <motion.section
            className="collection-stats"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="stats-grid">
              <div className="stat-card">
                <i className="fas fa-calendar-alt"></i>
                <h3>{collectionStats.lastCollection}</h3>
                <p>Last Collection</p>
              </div>
              <div className="stat-card">
                <i className="fas fa-users"></i>
                <h3>{collectionStats.totalPlayers.toLocaleString()}</h3>
                <p>Players Collected</p>
              </div>
              <div className="stat-card">
                <i className="fas fa-layer-group"></i>
                <h3>{collectionStats.seasonsCollected}</h3>
                <p>Seasons Analyzed</p>
              </div>
              <div className="stat-card">
                <i className="fas fa-clock"></i>
                <h3>{collectionStats.collectionTime}</h3>
                <p>Collection Time</p>
              </div>
            </div>
          </motion.section>
        )}

        {/* Data Sources */}
        <motion.section
          className="data-sources"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <h2>Data Sources</h2>
          <p>Reliable and comprehensive NBA data collection from multiple sources</p>

          <div className="sources-grid">
            {dataSources.map((source, index) => (
              <motion.div
                key={source.name}
                className="source-card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
              >
                <div className="source-header">
                  <div className="source-icon" style={{ backgroundColor: source.color }}>
                    <i className={source.icon}></i>
                  </div>
                  <div className="source-info">
                    <h3>{source.name}</h3>
                    <span className={`status ${source.status.toLowerCase()}`}>
                      {source.status}
                    </span>
                  </div>
                </div>
                <p className="source-description">{source.description}</p>
                <div className="source-details">
                  <div className="detail-item">
                    <strong>Last Update:</strong> {source.lastUpdate}
                  </div>
                  <div className="detail-item">
                    <strong>Data Points:</strong> {source.dataPoints}
                  </div>
                </div>
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
        </motion.section>

        {/* Scraping Features */}
        <motion.section
          className="scraping-features"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h2>Web Scraping Features</h2>
          <p>Advanced data collection capabilities and automation</p>

          <div className="features-grid">
            {scrapingFeatures.map((feature, index) => (
              <motion.div
                key={feature.title}
                className="feature-card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.8 + index * 0.1 }}
              >
                <div className="feature-icon">
                  <i className={feature.icon}></i>
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
                <ul className="feature-details">
                  {feature.details.map((detail, idx) => (
                    <li key={idx}>{detail}</li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Collection Controls */}
        <motion.section
          className="collection-controls"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
        >
          <div className="controls-card">
            <h3>Manual Data Collection</h3>
            <p>Trigger data collection for specific seasons or sources</p>

            <div className="controls-form">
              <div className="form-group">
                <label htmlFor="season">Season</label>
                <select
                  id="season"
                  value={selectedSeason}
                  onChange={(e) => setSelectedSeason(e.target.value)}
                  className="form-select"
                >
                  <option value="2024">2023-24</option>
                  <option value="2023">2022-23</option>
                  <option value="2022">2021-22</option>
                  <option value="2021">2020-21</option>
                  <option value="2020">2019-20</option>
                </select>
              </div>

              <button
                className={`btn btn-primary ${isCollecting ? 'loading' : ''}`}
                onClick={handleStartCollection}
                disabled={isCollecting}
              >
                {isCollecting ? (
                  <>
                    <div className="spinner"></div>
                    Collecting Data...
                  </>
                ) : (
                  <>
                    <i className="fas fa-download"></i>
                    Start Collection
                  </>
                )}
              </button>
            </div>
          </div>
        </motion.section>

        {/* Technical Details */}
        <motion.section
          className="technical-details"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.2 }}
        >
          <h2>Technical Implementation</h2>
          <div className="details-grid">
            <div className="detail-card">
              <h3>Web Scraping Technology</h3>
              <ul>
                <li><strong>Python Libraries:</strong> BeautifulSoup4, Requests, Selenium</li>
                <li><strong>Data Processing:</strong> Pandas, NumPy for data manipulation</li>
                <li><strong>Error Handling:</strong> Robust retry mechanisms and logging</li>
                <li><strong>Rate Limiting:</strong> Respectful scraping with delays</li>
              </ul>
            </div>

            <div className="detail-card">
              <h3>Data Pipeline</h3>
              <ul>
                <li><strong>Collection:</strong> Automated scraping from multiple sources</li>
                <li><strong>Cleaning:</strong> Data validation and preprocessing</li>
                <li><strong>Storage:</strong> Structured data storage in CSV/JSON formats</li>
                <li><strong>Analysis:</strong> Integration with analysis modules</li>
              </ul>
            </div>

            <div className="detail-card">
              <h3>Monitoring & Maintenance</h3>
              <ul>
                <li><strong>Status Monitoring:</strong> Real-time collection status</li>
                <li><strong>Error Logging:</strong> Comprehensive error tracking</li>
                <li><strong>Performance Metrics:</strong> Collection time and success rates</li>
                <li><strong>Data Quality:</strong> Validation and quality checks</li>
              </ul>
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  );
};

export default DataCollection;