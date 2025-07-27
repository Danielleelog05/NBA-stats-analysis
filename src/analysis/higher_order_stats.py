"""
Higher-Order Statistics Calculation Module

This module calculates advanced NBA metrics from basic box score statistics,
including shooting efficiency, rebounding percentages, playmaking metrics,
and overall impact measures.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class HigherOrderStats:
    """Calculate higher-order NBA statistics from basic box score data."""

    def __init__(self):
        # League average pace factor (approximate, can be updated)
        self.league_pace = 100.0

    def calculate_efg_percentage(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Effective Field Goal Percentage.

        Formula: (FG + 0.5 * 3P) / FGA

        Args:
            df (pd.DataFrame): DataFrame with 'fg', 'fg3', 'fga' columns

        Returns:
            pd.Series: Effective field goal percentage
        """
        if not all(col in df.columns for col in ['fg', 'fg3', 'fga']):
            logger.warning("Missing required columns for eFG% calculation")
            return pd.Series([0] * len(df))

        efg = (df['fg'] + 0.5 * df['fg3']) / df['fga']
        return efg.fillna(0)

    def calculate_ts_percentage(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate True Shooting Percentage.

        Formula: PTS / (2 * (FGA + 0.44 * FTA))

        Args:
            df (pd.DataFrame): DataFrame with 'pts', 'fga', 'fta' columns

        Returns:
            pd.Series: True shooting percentage
        """
        if not all(col in df.columns for col in ['pts', 'fga', 'fta']):
            logger.warning("Missing required columns for TS% calculation")
            return pd.Series([0] * len(df))

        ts = df['pts'] / (2 * (df['fga'] + 0.44 * df['fta']))
        return ts.fillna(0)

    def calculate_rebound_percentages(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate rebounding percentages (simplified version).

        Note: True rebounding percentages require team and opponent data.
        This is a simplified calculation based on per-game stats.

        Args:
            df (pd.DataFrame): DataFrame with rebounding columns

        Returns:
            Dict[str, pd.Series]: Dictionary with OREB%, DREB%, TREB%
        """
        if not all(col in df.columns for col in ['orb', 'drb', 'trb', 'mp']):
            logger.warning("Missing required columns for rebounding % calculation")
            return {
                'oreb_pct': pd.Series([0] * len(df)),
                'dreb_pct': pd.Series([0] * len(df)),
                'treb_pct': pd.Series([0] * len(df))
            }

        # Simplified calculation based on per-36 minutes
        minutes_factor = 36 / df['mp']

        oreb_pct = (df['orb'] * minutes_factor) / 10  # Approximate
        dreb_pct = (df['drb'] * minutes_factor) / 30  # Approximate
        treb_pct = (df['trb'] * minutes_factor) / 40  # Approximate

        return {
            'oreb_pct': oreb_pct.fillna(0),
            'dreb_pct': dreb_pct.fillna(0),
            'treb_pct': treb_pct.fillna(0)
        }

    def calculate_assist_percentage(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Assist Percentage (simplified).

        Formula: (AST / MP) / (Team AST / Team MP) * 100
        Simplified version using league averages.

        Args:
            df (pd.DataFrame): DataFrame with 'ast', 'mp' columns

        Returns:
            pd.Series: Assist percentage
        """
        if not all(col in df.columns for col in ['ast', 'mp']):
            logger.warning("Missing required columns for AST% calculation")
            return pd.Series([0] * len(df))

        # Simplified calculation using league average assist rate
        league_ast_rate = 0.20  # Approximate league average
        ast_pct = (df['ast'] / df['mp']) / league_ast_rate * 100
        return ast_pct.fillna(0)

    def calculate_turnover_percentage(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Turnover Percentage.

        Formula: TOV / (FGA + 0.44 * FTA + TOV) * 100

        Args:
            df (pd.DataFrame): DataFrame with 'tov', 'fga', 'fta' columns

        Returns:
            pd.Series: Turnover percentage
        """
        if not all(col in df.columns for col in ['tov', 'fga', 'fta']):
            logger.warning("Missing required columns for TOV% calculation")
            return pd.Series([0] * len(df))

        tov_pct = df['tov'] / (df['fga'] + 0.44 * df['fta'] + df['tov']) * 100
        return tov_pct.fillna(0)

    def calculate_assist_to_turnover_ratio(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Assist-to-Turnover Ratio.

        Formula: AST / TOV

        Args:
            df (pd.DataFrame): DataFrame with 'ast', 'tov' columns

        Returns:
            pd.Series: Assist-to-turnover ratio
        """
        if not all(col in df.columns for col in ['ast', 'tov']):
            logger.warning("Missing required columns for AST/TO calculation")
            return pd.Series([0] * len(df))

        ast_to = df['ast'] / df['tov']
        return ast_to.fillna(0)

    def calculate_usage_percentage(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Usage Percentage (simplified).

        Formula: (FGA + 0.44 * FTA + TOV) * 100 / (MP * Team Pace)
        Simplified version using league average pace.

        Args:
            df (pd.DataFrame): DataFrame with 'fga', 'fta', 'tov', 'mp' columns

        Returns:
            pd.Series: Usage percentage
        """
        if not all(col in df.columns for col in ['fga', 'fta', 'tov', 'mp']):
            logger.warning("Missing required columns for USG% calculation")
            return pd.Series([0] * len(df))

        possessions = df['fga'] + 0.44 * df['fta'] + df['tov']
        usg_pct = possessions * 100 / (df['mp'] * self.league_pace / 48)
        return usg_pct.fillna(0)

    def calculate_game_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Game Score.

        Formula: PTS + 0.4 * FG - 0.7 * FGA - 0.4 * (FTA - FT) + 0.7 * ORB +
                0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV

        Args:
            df (pd.DataFrame): DataFrame with required columns

        Returns:
            pd.Series: Game score
        """
        required_cols = ['pts', 'fg', 'fga', 'fta', 'ft', 'orb', 'drb', 'stl', 'ast', 'blk', 'pf', 'tov']

        if not all(col in df.columns for col in required_cols):
            logger.warning("Missing required columns for Game Score calculation")
            return pd.Series([0] * len(df))

        game_score = (
            df['pts'] +
            0.4 * df['fg'] -
            0.7 * df['fga'] -
            0.4 * (df['fta'] - df['ft']) +
            0.7 * df['orb'] +
            0.3 * df['drb'] +
            df['stl'] +
            0.7 * df['ast'] +
            0.7 * df['blk'] -
            0.4 * df['pf'] -
            df['tov']
        )

        return game_score.fillna(0)

    def calculate_per(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate Player Efficiency Rating (simplified version).

        This is a simplified PER calculation. The full formula is complex
        and requires league averages and team data.

        Args:
            df (pd.DataFrame): DataFrame with required columns

        Returns:
            pd.Series: Simplified PER
        """
        # Simplified PER calculation
        if not all(col in df.columns for col in ['pts', 'ast', 'trb', 'stl', 'blk', 'tov', 'fg', 'fga', 'ft', 'fta']):
            logger.warning("Missing required columns for PER calculation")
            return pd.Series([0] * len(df))

        # Basic PER components
        scoring = df['pts'] * 1.0
        assists = df['ast'] * 2.0
        rebounds = df['trb'] * 1.0
        steals = df['stl'] * 2.0
        blocks = df['blk'] * 2.0
        turnovers = df['tov'] * -1.0

        # Shooting efficiency component
        shooting = (df['fg'] - df['fga'] * 0.5) * 1.0 + (df['ft'] - df['fta'] * 0.5) * 1.0

        per = scoring + assists + rebounds + steals + blocks + turnovers + shooting

        # Normalize to typical PER scale (15 = average)
        per = per / 10 + 15

        return per.fillna(15)

    def calculate_all_higher_order_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all higher-order statistics for a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame with basic NBA statistics

        Returns:
            pd.DataFrame: Original DataFrame with added higher-order statistics
        """
        if df.empty:
            logger.warning("Empty DataFrame provided")
            return df

        result_df = df.copy()

        # Calculate shooting efficiency metrics
        result_df['efg_pct'] = self.calculate_efg_percentage(df)
        result_df['ts_pct'] = self.calculate_ts_percentage(df)

        # Calculate rebounding percentages
        reb_pcts = self.calculate_rebound_percentages(df)
        result_df['oreb_pct'] = reb_pcts['oreb_pct']
        result_df['dreb_pct'] = reb_pcts['dreb_pct']
        result_df['treb_pct'] = reb_pcts['treb_pct']

        # Calculate playmaking metrics
        result_df['ast_pct'] = self.calculate_assist_percentage(df)
        result_df['tov_pct'] = self.calculate_turnover_percentage(df)
        result_df['ast_to_ratio'] = self.calculate_assist_to_turnover_ratio(df)

        # Calculate usage
        result_df['usg_pct'] = self.calculate_usage_percentage(df)

        # Calculate overall impact metrics
        result_df['game_score'] = self.calculate_game_score(df)
        result_df['per'] = self.calculate_per(df)

        logger.info(f"Calculated higher-order stats for {len(result_df)} players")
        return result_df

    def get_stat_descriptions(self) -> Dict[str, str]:
        """
        Get descriptions of all calculated higher-order statistics.

        Returns:
            Dict[str, str]: Dictionary mapping stat names to descriptions
        """
        return {
            'efg_pct': 'Effective Field Goal Percentage - Accounts for 3-point shooting',
            'ts_pct': 'True Shooting Percentage - Accounts for all shooting efficiency',
            'oreb_pct': 'Offensive Rebound Percentage - % of available offensive rebounds grabbed',
            'dreb_pct': 'Defensive Rebound Percentage - % of available defensive rebounds grabbed',
            'treb_pct': 'Total Rebound Percentage - % of available total rebounds grabbed',
            'ast_pct': 'Assist Percentage - % of teammate field goals assisted while on floor',
            'tov_pct': 'Turnover Percentage - Turnovers per 100 possessions',
            'ast_to_ratio': 'Assist-to-Turnover Ratio - Ball control efficiency',
            'usg_pct': 'Usage Percentage - % of team possessions used while on floor',
            'game_score': 'Game Score - Overall statistical contribution in a game',
            'per': 'Player Efficiency Rating - Overall player efficiency metric'
        }

def main():
    """Test the higher-order statistics calculation."""
    from src.data_collection.nba_scraper import NBADataScraper

    # Load sample data
    scraper = NBADataScraper()
    sample_df = scraper.load_sample_data()

    # Calculate higher-order stats
    calculator = HigherOrderStats()
    enhanced_df = calculator.calculate_all_higher_order_stats(sample_df)

    # Display results
    print("Higher-Order Statistics Calculated:")
    print("=" * 50)

    stats_to_show = ['player', 'efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per']
    display_df = enhanced_df[stats_to_show].round(3)
    print(display_df.to_string(index=False))

    # Save enhanced data
    enhanced_df.to_csv("data/processed/nba_enhanced_stats.csv", index=False)
    print(f"\nEnhanced data saved to data/processed/nba_enhanced_stats.csv")

if __name__ == "__main__":
    main()