# NBA Stats Analysis - React Web Application

A modern, interactive web application for NBA player performance analysis with advanced analytics, data visualization, and comprehensive player insights.

## 🏀 Features

### Core Functionality
- **Interactive Dashboard**: Real-time analytics with dynamic charts and statistics
- **Player Analysis**: Comprehensive player comparison and strength evaluation
- **Data Collection**: Automated web scraping from multiple NBA sources
- **Advanced Visualizations**: Radar charts, bar charts, line charts, and more
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### Web Scraping Capabilities
- **Automated Data Collection**: Scheduled scraping from Basketball Reference, NBA.com, and Kaggle
- **Multi-Source Integration**: Aggregates data from multiple reliable sources
- **Real-time Monitoring**: Live status tracking and error handling
- **Data Processing Pipeline**: Automated cleaning and preprocessing

### Analytics Features
- **Higher-Order Statistics**: Advanced metrics beyond traditional box scores
- **Player Strength Model**: Quantifiable player evaluation system
- **Performance Trends**: Historical analysis and trend identification
- **Comparative Analysis**: Side-by-side player comparisons

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nba-stats-analysis
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   └── layout/         # Header, Footer, Navigation
├── pages/              # Main application pages
│   ├── Home.js         # Landing page
│   ├── Dashboard.js    # Analytics dashboard
│   ├── PlayerAnalysis.js # Player comparison tools
│   ├── DataCollection.js # Web scraping interface
│   └── About.js        # Project information
├── hooks/              # Custom React hooks
├── utils/              # Utility functions
├── styles/             # CSS and styling
└── assets/             # Images and static files
```

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing
- **Framer Motion**: Smooth animations and transitions
- **Recharts**: Interactive data visualizations
- **Styled Components**: CSS-in-JS styling
- **React Query**: Data fetching and caching

### Data Visualization
- **Recharts**: Bar charts, line charts, radar charts
- **D3.js**: Advanced custom visualizations
- **Victory**: Additional chart components

### UI/UX
- **Font Awesome**: Icon library
- **Google Fonts**: Typography
- **CSS Variables**: Design system
- **Responsive Design**: Mobile-first approach

## 📊 Data Sources

### Primary Sources
1. **Basketball Reference** (`basketball-reference.com`)
   - Comprehensive NBA statistics
   - Historical data and advanced metrics
   - Player and team statistics

2. **NBA.com Stats** (`nba.com/stats`)
   - Official NBA statistics
   - Advanced player tracking data
   - Real-time game statistics

3. **Kaggle Datasets**
   - Curated basketball datasets
   - Historical player data
   - Team performance records

### Data Collection Process
1. **Automated Scraping**: Python scripts with BeautifulSoup4 and Selenium
2. **Data Validation**: Quality checks and error handling
3. **Processing Pipeline**: Cleaning and preprocessing
4. **Storage**: Structured data in CSV/JSON formats
5. **API Integration**: RESTful API for frontend consumption

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0
```

### API Configuration
The app is configured to proxy API requests to `http://localhost:8000` (your Python backend).

## 📈 Features in Detail

### Dashboard
- **Real-time Statistics**: Live player and team statistics
- **Interactive Charts**: Dynamic visualizations with filtering
- **Performance Metrics**: PPG, RPG, APG, efficiency ratings
- **Trend Analysis**: Season-over-season comparisons

### Player Analysis
- **Radar Charts**: Multi-dimensional player comparison
- **Statistical Comparison**: Side-by-side stat analysis
- **Strength Evaluation**: Player tier categorization
- **Advanced Insights**: PER, VORP, Win Shares analysis

### Data Collection
- **Source Monitoring**: Real-time status of data sources
- **Collection Controls**: Manual trigger for data updates
- **Error Handling**: Comprehensive logging and alerts
- **Performance Metrics**: Collection time and success rates

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Various Platforms

#### Netlify
1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set publish directory: `build`

#### Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel --prod`

#### GitHub Pages
1. Add to package.json:
   ```json
   "homepage": "https://username.github.io/repo-name",
   "scripts": {
     "predeploy": "npm run build",
     "deploy": "gh-pages -d build"
   }
   ```
2. Deploy: `npm run deploy`

## 🔒 Security Considerations

### Data Privacy
- No personal player information stored
- Public statistics only
- Respectful web scraping practices

### Rate Limiting
- Implemented delays between requests
- Respectful to source websites
- Error handling for blocked requests

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -m 'Add feature'`
6. Push: `git push origin feature-name`
7. Create a Pull Request

### Code Style
- Use functional components with hooks
- Follow React best practices
- Maintain consistent naming conventions
- Add proper TypeScript types (if using TS)

## 📝 API Documentation

### Endpoints (Backend Integration)

#### Player Data
```
GET /api/players
GET /api/players/:id
GET /api/players/:id/stats
```

#### Analytics
```
GET /api/analytics/dashboard
GET /api/analytics/player/:id
GET /api/analytics/comparison
```

#### Data Collection
```
POST /api/collection/start
GET /api/collection/status
GET /api/collection/sources
```

## 🐛 Troubleshooting

### Common Issues

#### Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Chart Rendering Issues
- Ensure container has proper dimensions
- Check for missing data
- Verify chart configuration

#### API Connection Issues
- Check backend server is running
- Verify proxy configuration
- Check CORS settings

## 📊 Performance Optimization

### Best Practices
- **Code Splitting**: Lazy load components
- **Memoization**: Use React.memo and useMemo
- **Image Optimization**: Compress and lazy load images
- **Bundle Analysis**: Monitor bundle size

### Monitoring
- **Lighthouse**: Performance auditing
- **Web Vitals**: Core Web Vitals tracking
- **Error Tracking**: Sentry integration

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Basketball Reference for comprehensive statistics
- NBA.com for official data
- Kaggle community for datasets
- React and open-source community

## 📞 Support

For questions or support:
- Create an issue on GitHub
- Email: contact@nba-stats-analysis.com
- Documentation: [Link to docs]

---

**Built with ❤️ for basketball analytics**