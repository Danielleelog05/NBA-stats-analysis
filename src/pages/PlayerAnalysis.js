import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import './PlayerAnalysis.css';

const PlayerAnalysis = () => {
  const [selectedPlayer1, setSelectedPlayer1] = useState('Nikola Jokić');
  const [selectedPlayer2, setSelectedPlayer2] = useState('Joel Embiid');
  const [analysisType, setAnalysisType] = useState('comparison');

  // Mock data for demonstration
  const { data: playerData, isLoading } = useQuery('playerData', async () => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      players: [
        {
          name: 'Nikola Jokić',
          team: 'DEN',
          position: 'C',
          stats: {
            ppg: 28.2,
            rpg: 12.8,
            apg: 8.9,
            spg: 1.2,
            bpg: 0.9,
            efg: 0.632,
            ts: 0.701,
            per: 31.2,
            ws: 12.8,
            vorp: 8.9
          },
          radarData: [
            { metric: 'Scoring', value: 85 },
            { metric: 'Rebounding', value: 90 },
            { metric: 'Playmaking', value: 95 },
            { metric: 'Defense', value: 70 },
            { metric: 'Efficiency', value: 95 },
            { metric: 'Impact', value: 95 }
          ]
        },
        {
          name: 'Joel Embiid',
          team: 'PHI',
          position: 'C',
          stats: {
            ppg: 35.1,
            rpg: 11.1,
            apg: 5.9,
            spg: 1.0,
            bpg: 1.7,
            efg: 0.598,
            ts: 0.665,
            per: 33.1,
            ws: 11.2,
            vorp: 7.8
          },
          radarData: [
            { metric: 'Scoring', value: 95 },
            { metric: 'Rebounding', value: 85 },
            { metric: 'Playmaking', value: 75 },
            { metric: 'Defense', value: 90 },
            { metric: 'Efficiency', value: 85 },
            { metric: 'Impact', value: 90 }
          ]
        },
        {
          name: 'Luka Dončić',
          team: 'DAL',
          position: 'PG',
          stats: {
            ppg: 33.9,
            rpg: 8.2,
            apg: 9.8,
            spg: 1.4,
            bpg: 0.5,
            efg: 0.587,
            ts: 0.623,
            per: 28.5,
            ws: 10.1,
            vorp: 6.9
          },
          radarData: [
            { metric: 'Scoring', value: 90 },
            { metric: 'Rebounding', value: 75 },
            { metric: 'Playmaking', value: 90 },
            { metric: 'Defense', value: 60 },
            { metric: 'Efficiency', value: 80 },
            { metric: 'Impact', value: 85 }
          ]
        }
      ],
      strengthCategories: [
        { category: 'Elite', count: 15, percentage: 3.3 },
        { category: 'All-Star', count: 45, percentage: 10.0 },
        { category: 'Starter', count: 150, percentage: 33.3 },
        { category: 'Role Player', count: 180, percentage: 40.0 },
        { category: 'Bench', count: 60, percentage: 13.3 }
      ]
    };
  });

  const analysisTypes = [
    { key: 'comparison', label: 'Player Comparison', icon: 'fas fa-balance-scale' },
    { key: 'strength', label: 'Strength Analysis', icon: 'fas fa-chart-line' },
    { key: 'trends', label: 'Performance Trends', icon: 'fas fa-trending-up' },
    { key: 'insights', label: 'Advanced Insights', icon: 'fas fa-lightbulb' }
  ];

  if (isLoading) {
    return (
      <div className="player-analysis">
        <div className="container">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading player analysis data...</p>
          </div>
        </div>
      </div>
    );
  }

  const player1 = playerData.players.find(p => p.name === selectedPlayer1);
  const player2 = playerData.players.find(p => p.name === selectedPlayer2);

  return (
    <div className="player-analysis">
      <div className="container">
        {/* Header */}
        <motion.div
          className="analysis-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1>Player Analysis</h1>
          <p>Comprehensive player performance analysis and comparison tools</p>
        </motion.div>

        {/* Analysis Type Selector */}
        <motion.div
          className="analysis-types"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="type-selector">
            {analysisTypes.map((type) => (
              <button
                key={type.key}
                className={`type-btn ${analysisType === type.key ? 'active' : ''}`}
                onClick={() => setAnalysisType(type.key)}
              >
                <i className={type.icon}></i>
                <span>{type.label}</span>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Player Selection */}
        <motion.div
          className="player-selection"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="selection-grid">
            <div className="player-selector">
              <label htmlFor="player1">Player 1</label>
              <select
                id="player1"
                value={selectedPlayer1}
                onChange={(e) => setSelectedPlayer1(e.target.value)}
                className="form-select"
              >
                {playerData.players.map(player => (
                  <option key={player.name} value={player.name}>
                    {player.name} ({player.team})
                  </option>
                ))}
              </select>
            </div>
            <div className="player-selector">
              <label htmlFor="player2">Player 2</label>
              <select
                id="player2"
                value={selectedPlayer2}
                onChange={(e) => setSelectedPlayer2(e.target.value)}
                className="form-select"
              >
                {playerData.players.map(player => (
                  <option key={player.name} value={player.name}>
                    {player.name} ({player.team})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </motion.div>

        {/* Analysis Content */}
        {analysisType === 'comparison' && (
          <motion.div
            className="comparison-analysis"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <div className="comparison-grid">
              {/* Radar Chart Comparison */}
              <div className="chart-container">
                <div className="chart-header">
                  <h2>Player Comparison - Radar Chart</h2>
                </div>
                <div className="chart-content">
                  <ResponsiveContainer width="100%" height={400}>
                    <RadarChart data={player1.radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="metric" />
                      <PolarRadiusAxis angle={90} domain={[0, 100]} />
                      <Radar
                        name={player1.name}
                        dataKey="value"
                        stroke="#3b82f6"
                        fill="#3b82f6"
                        fillOpacity={0.3}
                      />
                      <Radar
                        name={player2.name}
                        dataKey="value"
                        stroke="#ef4444"
                        fill="#ef4444"
                        fillOpacity={0.3}
                      />
                      <Tooltip />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Stats Comparison */}
              <div className="stats-comparison">
                <div className="comparison-table">
                  <h3>Statistical Comparison</h3>
                  <table>
                    <thead>
                      <tr>
                        <th>Statistic</th>
                        <th>{player1.name}</th>
                        <th>{player2.name}</th>
                        <th>Difference</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(player1.stats).map(([stat, value]) => {
                        const player2Value = player2.stats[stat];
                        const difference = value - player2Value;
                        const isPositive = difference > 0;

                        return (
                          <tr key={stat}>
                            <td>{stat.toUpperCase()}</td>
                            <td>{typeof value === 'number' ? value.toFixed(1) : value}</td>
                            <td>{typeof player2Value === 'number' ? player2Value.toFixed(1) : player2Value}</td>
                            <td className={isPositive ? 'positive' : 'negative'}>
                              {isPositive ? '+' : ''}{difference.toFixed(1)}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {analysisType === 'strength' && (
          <motion.div
            className="strength-analysis"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <div className="strength-grid">
              {/* Player Strength Distribution */}
              <div className="chart-container">
                <div className="chart-header">
                  <h2>Player Strength Distribution</h2>
                </div>
                <div className="chart-content">
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={playerData.strengthCategories}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="category" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Strength Categories */}
              <div className="strength-categories">
                <h3>Strength Categories</h3>
                <div className="categories-grid">
                  {playerData.strengthCategories.map((category, index) => (
                    <div key={category.category} className="category-card">
                      <div className="category-header">
                        <h4>{category.category}</h4>
                        <span className="percentage">{category.percentage}%</span>
                      </div>
                      <div className="category-count">{category.count} players</div>
                      <div className="category-bar">
                        <div
                          className="bar-fill"
                          style={{ width: `${category.percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Player Insights */}
        <motion.div
          className="player-insights"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <div className="insights-grid">
            <div className="insight-card">
              <div className="insight-header">
                <i className="fas fa-star"></i>
                <h3>Key Strengths</h3>
              </div>
              <ul>
                <li>Exceptional playmaking ability for a center</li>
                <li>High efficiency scoring with excellent shooting percentages</li>
                <li>Strong rebounding and defensive presence</li>
                <li>Consistent performance across multiple seasons</li>
              </ul>
            </div>

            <div className="insight-card">
              <div className="insight-header">
                <i className="fas fa-chart-line"></i>
                <h3>Performance Trends</h3>
              </div>
              <ul>
                <li>Steady improvement in scoring efficiency</li>
                <li>Maintained high assist numbers despite increased scoring</li>
                <li>Consistent rebounding production</li>
                <li>Improved defensive metrics over time</li>
              </ul>
            </div>

            <div className="insight-card">
              <div className="insight-header">
                <i className="fas fa-lightbulb"></i>
                <h3>Advanced Insights</h3>
              </div>
              <ul>
                <li>Elite PER rating indicates exceptional overall impact</li>
                <li>High VORP suggests significant value over replacement</li>
                <li>Strong win shares contribution to team success</li>
                <li>Excellent true shooting percentage efficiency</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PlayerAnalysis;