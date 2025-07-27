import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import PlayerAnalysis from './pages/PlayerAnalysis';
import DataCollection from './pages/DataCollection';
import About from './pages/About';
import './App.css';

function App() {
  return (
    <div className="App">
      <Helmet>
        <title>NBA Stats Analysis - Beyond the Box Score</title>
        <meta name="description" content="Interactive NBA player performance analysis with higher-order statistics and advanced metrics" />
        <meta name="keywords" content="NBA, basketball, statistics, player analysis, advanced metrics, basketball analytics" />
        <meta property="og:title" content="NBA Stats Analysis" />
        <meta property="og:description" content="Interactive NBA player performance analysis" />
        <meta property="og:type" content="website" />
      </Helmet>

      <Header />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/player-analysis" element={<PlayerAnalysis />} />
          <Route path="/data-collection" element={<DataCollection />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default App;