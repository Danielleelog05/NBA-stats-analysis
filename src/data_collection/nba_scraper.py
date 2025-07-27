"""
NBA Data Collection Module

This module handles the collection of NBA player statistics from various sources,
primarily Basketball-Reference.com, and includes data cleaning and preprocessing.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NBADataScraper:
    """NBA Data Scraper for collecting player statistics."""

    def __init__(self, base_url: str = "https://www.basketball-reference.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_season_stats(self, season: int) -> pd.DataFrame:
        """
        Scrape player statistics for a specific NBA season.

        Args:
            season (int): NBA season (e.g., 2024 for 2023-24 season)

        Returns:
            pd.DataFrame: DataFrame containing player statistics
        """
        url = f"{self.base_url}/leagues/NBA_{season}_per_game.html"

        try:
            logger.info(f"Scraping data for {season}-{season+1} season...")
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': 'per_game_stats'})

            if not table:
                raise ValueError(f"Could not find stats table for season {season}")

            # Extract data
            data = []
            rows = table.find('tbody').find_all('tr')

            for row in rows:
                # Skip summary rows
                if 'thead' in row.get('class', []):
                    continue

                cells = row.find_all(['td', 'th'])
                row_data = {}

                for i, cell in enumerate(cells):
                    if cell.get('data-stat'):
                        stat_name = cell.get('data-stat')
                        value = cell.get_text(strip=True)
                        row_data[stat_name] = value

                if row_data:  # Only add non-empty rows
                    data.append(row_data)

            df = pd.DataFrame(data)
            logger.info(f"Successfully scraped {len(df)} players for {season}-{season+1} season")
            return df

        except Exception as e:
            logger.error(f"Error scraping season {season}: {str(e)}")
            return pd.DataFrame()

    def get_multiple_seasons(self, start_season: int, end_season: int) -> Dict[int, pd.DataFrame]:
        """
        Scrape data for multiple seasons.

        Args:
            start_season (int): Starting season
            end_season (int): Ending season

        Returns:
            Dict[int, pd.DataFrame]: Dictionary mapping seasons to DataFrames
        """
        season_data = {}

        for season in range(start_season, end_season + 1):
            df = self.get_season_stats(season)
            if not df.empty:
                season_data[season] = df
                # Be respectful with requests
                time.sleep(2)

        return season_data

    def clean_player_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess player statistics data.

        Args:
            df (pd.DataFrame): Raw player statistics DataFrame

        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        if df.empty:
            return df

        # Create a copy to avoid modifying original
        cleaned_df = df.copy()

        # Convert numeric columns
        numeric_columns = [
            'g', 'gs', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
            'fg2', 'fg2a', 'fg2_pct', 'efg_pct', 'ft', 'fta', 'ft_pct',
            'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts'
        ]

        for col in numeric_columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')

        # Handle missing values
        cleaned_df = cleaned_df.fillna(0)

        # Filter for minimum playing time (e.g., 10 minutes per game)
        if 'mp' in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df['mp'] >= 10]

        # Filter for minimum games played (e.g., 20 games)
        if 'g' in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df['g'] >= 20]

        # Standardize player names
        if 'player' in cleaned_df.columns:
            cleaned_df['player'] = cleaned_df['player'].str.strip()

        # Standardize team abbreviations
        if 'team_id' in cleaned_df.columns:
            team_mapping = {
                'ATL': 'ATL', 'BOS': 'BOS', 'BRK': 'BKN', 'CHO': 'CHA',
                'CHI': 'CHI', 'CLE': 'CLE', 'DAL': 'DAL', 'DEN': 'DEN',
                'DET': 'DET', 'GSW': 'GSW', 'HOU': 'HOU', 'IND': 'IND',
                'LAC': 'LAC', 'LAL': 'LAL', 'MEM': 'MEM', 'MIA': 'MIA',
                'MIL': 'MIL', 'MIN': 'MIN', 'NOP': 'NOP', 'NYK': 'NYK',
                'OKC': 'OKC', 'ORL': 'ORL', 'PHI': 'PHI', 'PHO': 'PHX',
                'POR': 'POR', 'SAC': 'SAC', 'SAS': 'SAS', 'TOR': 'TOR',
                'UTA': 'UTA', 'WAS': 'WAS'
            }
            cleaned_df['team_id'] = cleaned_df['team_id'].map(team_mapping).fillna(cleaned_df['team_id'])

        logger.info(f"Cleaned data: {len(cleaned_df)} players remaining")
        return cleaned_df

    def save_data(self, data: Dict[int, pd.DataFrame], output_dir: str = "data/raw"):
        """
        Save scraped data to CSV files.

        Args:
            data (Dict[int, pd.DataFrame]): Dictionary of season data
            output_dir (str): Output directory for saving files
        """
        os.makedirs(output_dir, exist_ok=True)

        for season, df in data.items():
            if not df.empty:
                filename = f"{output_dir}/nba_stats_{season}_{season+1}.csv"
                df.to_csv(filename, index=False)
                logger.info(f"Saved {filename} with {len(df)} players")

    def load_sample_data(self) -> pd.DataFrame:
        """
        Load sample data for testing and development.
        This creates a small dataset with realistic NBA statistics.

        Returns:
            pd.DataFrame: Sample NBA player statistics
        """
        sample_data = {
            'player': ['LeBron James', 'Stephen Curry', 'Kevin Durant', 'Giannis Antetokounmpo', 'Nikola Jokic'],
            'team_id': ['LAL', 'GSW', 'PHX', 'MIL', 'DEN'],
            'g': [55, 56, 47, 63, 69],
            'gs': [54, 56, 47, 63, 69],
            'mp': [35.5, 32.7, 37.2, 32.1, 33.7],
            'fg': [8.2, 8.8, 9.1, 10.3, 8.9],
            'fga': [16.5, 18.3, 17.2, 18.4, 14.8],
            'fg_pct': [0.497, 0.481, 0.529, 0.560, 0.601],
            'fg3': [1.8, 4.4, 2.1, 0.8, 1.1],
            'fg3a': [5.4, 11.4, 5.1, 2.8, 3.0],
            'fg3_pct': [0.333, 0.386, 0.412, 0.286, 0.367],
            'ft': [4.8, 4.2, 6.1, 7.8, 5.9],
            'fta': [6.2, 4.6, 6.8, 9.6, 6.8],
            'ft_pct': [0.774, 0.913, 0.897, 0.813, 0.868],
            'orb': [1.1, 0.6, 0.7, 1.8, 2.9],
            'drb': [6.2, 4.1, 6.4, 8.2, 8.9],
            'trb': [7.3, 4.7, 7.1, 10.0, 11.8],
            'ast': [7.3, 6.3, 5.6, 5.7, 9.8],
            'stl': [1.1, 0.9, 0.8, 1.0, 1.2],
            'blk': [0.6, 0.4, 1.2, 0.8, 0.7],
            'tov': [3.5, 3.2, 3.1, 3.4, 3.6],
            'pf': [1.8, 2.0, 2.1, 2.8, 2.4],
            'pts': [25.0, 26.4, 29.9, 30.1, 24.5]
        }

        return pd.DataFrame(sample_data)

def main():
    """Main function to run the scraper."""
    scraper = NBADataScraper()

    # For development, use sample data
    logger.info("Loading sample data for development...")
    sample_df = scraper.load_sample_data()

    # Clean the sample data
    cleaned_df = scraper.clean_player_data(sample_df)

    # Save sample data
    os.makedirs("data/raw", exist_ok=True)
    cleaned_df.to_csv("data/raw/nba_sample_data.csv", index=False)
    logger.info("Sample data saved to data/raw/nba_sample_data.csv")

    # Uncomment below for actual scraping (be mindful of rate limits)
    """
    # Scrape recent seasons
    seasons_data = scraper.get_multiple_seasons(2020, 2024)

    # Clean all data
    cleaned_data = {}
    for season, df in seasons_data.items():
        cleaned_data[season] = scraper.clean_player_data(df)

    # Save data
    scraper.save_data(cleaned_data)
    """

if __name__ == "__main__":
    main()