# NBA Player Performance Analysis - Beyond the Box Score

A comprehensive system that analyzes basic NBA player statistics to compute and interpret higher-order metrics, ultimately evaluating a player's overall strength and impact with interactive visualizations.

## Project Overview

This project demonstrates how foundational NBA data can be leveraged to gain deeper insights into player performance through advanced analytics and compelling visualizations.

### Key Features

- **Data Acquisition**: Robust collection of NBA player statistics from multiple sources
- **Higher-Order Statistics**: Calculation of advanced metrics from basic box score data
- **Player Strength Evaluation**: Quantifiable model assigning strength scores to players
- **Interactive Visualizations**: Comprehensive plots and dashboards for exploration
- **Insights Report**: Summary of key findings and conclusions

## Project Structure

```
stats analysis/
├── data/                   # Data storage
│   ├── raw/               # Raw scraped data
│   └── processed/         # Cleaned and processed data
├── src/                   # Source code
│   ├── data_collection/   # Data acquisition modules
│   ├── analysis/          # Statistical analysis modules
│   ├── visualization/     # Plotting and visualization modules
│   └── models/           # Player strength evaluation models
├── notebooks/            # Jupyter notebooks for exploration
├── dashboards/           # Streamlit dashboards
├── reports/              # Generated reports and insights
└── tests/               # Unit tests
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start

1. **Data Collection**:
   ```bash
   python src/data_collection/nba_scraper.py
   ```

2. **Run Analysis**:
   ```bash
   python src/analysis/player_analysis.py
   ```

3. **Launch Dashboard**:
   ```bash
   streamlit run dashboards/main_dashboard.py
   ```

### Jupyter Notebooks

- `notebooks/01_data_exploration.ipynb`: Initial data exploration
- `notebooks/02_higher_order_stats.ipynb`: Higher-order statistics calculation
- `notebooks/03_player_strength_model.ipynb`: Player strength evaluation
- `notebooks/04_visualization_insights.ipynb`: Visualization and insights

## Higher-Order Statistics Calculated

- **Shooting Efficiency**: eFG%, TS%
- **Rebounding**: OREB%, DREB%, TREB%
- **Playmaking**: AST%, TOV%, AST/TO ratio
- **Usage**: USG%
- **Overall Impact**: PER, Game Score

## Player Strength Model

The system uses a weighted combination of higher-order statistics to evaluate player strength:

- Position-adjusted weighting schemes
- Normalized statistics for fair comparison
- Tier-based categorization (Elite, Starter, Role Player, Bench)

## Visualizations

- **Exploratory**: Histograms, box plots, scatter plots, correlation heatmaps
- **Player Comparison**: Bar charts, radar charts, strength/weakness plots
- **Overall Evaluation**: Ranked charts, distribution plots, interactive search
- **Time Series**: Player evolution over seasons

## Data Sources

- Basketball-Reference.com
- NBA.com/stats
- Kaggle NBA datasets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details