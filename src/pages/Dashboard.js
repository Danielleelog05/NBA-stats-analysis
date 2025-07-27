import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import './Dashboard.css';

const Dashboard = () => {
  const [selectedMetric, setSelectedMetric] = useState('ppg');
  const [selectedSeason, setSelectedSeason] = useState('2024');

  // Mock data for demonstration
  const { data: dashboardData, isLoading } = useQuery('dashboardData', async () => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      topPlayers: [
        { name: 'Nikola Jokić', team: 'DEN', ppg: 28.2, rpg: 12.8, apg: 8.9, efg: 0.632 },
        { name: 'Joel Embiid', team: 'PHI', ppg: 35.1, rpg: 11.1, apg: 5.9, efg: 0.598 },
        { name: 'Luka Dončić', team: 'DAL', ppg: 33.9, rpg: 8.2, apg: 9.8, efg: 0.587 },
        { name: 'Giannis Antetokounmpo', team: 'MIL', ppg: 30.8, rpg: 11.5, apg: 6.4, efg: 0.612 },
        { name: 'Kevin Durant', team: 'PHX', ppg: 29.9, rpg: 6.7, apg: 5.9, efg: 0.601 }
      ],
      seasonStats: [
        { season: '2020', avgPpg: 22.1, avgRpg: 8.9, avgApg: 5.2, avgEfg: 0.534 },
        { season: '2021', avgPpg: 22.8, avgRpg: 9.1, avgApg: 5.4, avgEfg: 0.541 },
        { season: '2022', avgPpg: 23.2, avgRpg: 9.3, avgApg: 5.6, avgEfg: 0.548 },
        { season: '2023', avgPpg: 23.8, avgRpg: 9.5, avgApg: 5.8, avgEfg: 0.552 },
        { season: '2024', avgPpg: 24.1, avgRpg: 9.7, avgApg: 6.0, avgEfg: 0.558 }
      ],
      positionDistribution: [
        { position: 'PG', count: 120, percentage: 26.7 },
        { position: 'SG', count: 115, percentage: 25.6 },
        { position: 'SF', count: 95, percentage: 21.1 },
        { position: 'PF', count: 80, percentage: 17.8 },
        { position: 'C', count: 40, percentage: 8.9 }
      ],
      teamPerformance: [
        { team: 'BOS', wins: 35, losses: 12, winRate: 0.745 },
        { team: 'MIL', wins: 33, losses: 14, winRate: 0.702 },
        { team: 'PHI', wins: 32, losses: 15, winRate: 0.681 },
        { team: 'DEN', wins: 31, losses: 16, winRate: 0.660 },
        { team: 'LAC', wins: 30, losses: 17, winRate: 0.638 }
      ]
    };
  });

  const metrics = [
    { key: 'ppg', label: 'Points Per Game', color: '#3b82f6' },
    { key: 'rpg', label: 'Rebounds Per Game', color: '#10b981' },
    { key: 'apg', label: 'Assists Per Game', color: '#f59e0b' },
    { key: 'efg', label: 'Effective FG%', color: '#ef4444' }
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (isLoading) {
    return (
      <div className="dashboard">
        <div className="container">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading dashboard data...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="container">
        {/* Header */}
        <motion.div
          className="dashboard-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1>NBA Analytics Dashboard</h1>
          <p>Comprehensive overview of player performance and team statistics</p>
        </motion.div>

        {/* Controls */}
        <motion.div
          className="dashboard-controls"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="controls-grid">
            <div className="control-group">
              <label htmlFor="metric">Metric</label>
              <select
                id="metric"
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value)}
                className="form-select"
              >
                {metrics.map(metric => (
                  <option key={metric.key} value={metric.key}>
                    {metric.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="control-group">
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
          </div>
        </motion.div>

        {/* Stats Overview */}
        <motion.div
          className="stats-overview"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Players</h3>
              <div className="stat-value">450</div>
              <div className="stat-change positive">+12 from last season</div>
            </div>
            <div className="stat-card">
              <h3>Average PPG</h3>
              <div className="stat-value">24.1</div>
              <div className="stat-change positive">+0.3 from last season</div>
            </div>
            <div className="stat-card">
              <h3>Average RPG</h3>
              <div className="stat-value">9.7</div>
              <div className="stat-change positive">+0.2 from last season</div>
            </div>
            <div className="stat-card">
              <h3>Average APG</h3>
              <div className="stat-value">6.0</div>
              <div className="stat-change positive">+0.2 from last season</div>
            </div>
          </div>
        </motion.div>

        {/* Charts Section */}
        <div className="charts-section">
          {/* Top Players Chart */}
          <motion.div
            className="chart-container"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <div className="chart-header">
              <h2>Top Players by {metrics.find(m => m.key === selectedMetric)?.label}</h2>
            </div>
            <div className="chart-content">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={dashboardData.topPlayers}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey={selectedMetric} fill={metrics.find(m => m.key === selectedMetric)?.color} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Season Trends */}
          <motion.div
            className="chart-container"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <div className="chart-header">
              <h2>Season Trends</h2>
            </div>
            <div className="chart-content">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={dashboardData.seasonStats}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="season" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="avgPpg" stroke="#3b82f6" name="Avg PPG" />
                  <Line type="monotone" dataKey="avgRpg" stroke="#10b981" name="Avg RPG" />
                  <Line type="monotone" dataKey="avgApg" stroke="#f59e0b" name="Avg APG" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Position Distribution */}
          <motion.div
            className="chart-container"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.0 }}
          >
            <div className="chart-header">
              <h2>Position Distribution</h2>
            </div>
            <div className="chart-content">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={dashboardData.positionDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ position, percentage }) => `${position} ${percentage}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {dashboardData.positionDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Team Performance */}
          <motion.div
            className="chart-container"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.2 }}
          >
            <div className="chart-header">
              <h2>Team Win Rates</h2>
            </div>
            <div className="chart-content">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={dashboardData.teamPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="team" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="winRate" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        </div>

        {/* Top Players Table */}
        <motion.div
          className="players-table"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.4 }}
        >
          <div className="table-header">
            <h2>Top Players</h2>
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Player</th>
                  <th>Team</th>
                  <th>PPG</th>
                  <th>RPG</th>
                  <th>APG</th>
                  <th>eFG%</th>
                </tr>
              </thead>
              <tbody>
                {dashboardData.topPlayers.map((player, index) => (
                  <tr key={player.name}>
                    <td>{index + 1}</td>
                    <td>{player.name}</td>
                    <td>{player.team}</td>
                    <td>{player.ppg}</td>
                    <td>{player.rpg}</td>
                    <td>{player.apg}</td>
                    <td>{(player.efg * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;