"""
Player Strength Evaluation Model

This module implements a comprehensive model for evaluating NBA player strength
based on higher-order statistics with position-adjusted weighting schemes.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class PlayerStrengthModel:
    """Player strength evaluation model using higher-order statistics."""

    def __init__(self):
        # Position-based weighting schemes
        self.position_weights = {
            'PG': {
                'efg_pct': 0.15, 'ts_pct': 0.15, 'ast_pct': 0.20, 'tov_pct': 0.10,
                'usg_pct': 0.10, 'ast_to_ratio': 0.15, 'per': 0.15
            },
            'SG': {
                'efg_pct': 0.20, 'ts_pct': 0.20, 'ast_pct': 0.10, 'tov_pct': 0.10,
                'usg_pct': 0.15, 'ast_to_ratio': 0.10, 'per': 0.15
            },
            'SF': {
                'efg_pct': 0.15, 'ts_pct': 0.15, 'ast_pct': 0.10, 'tov_pct': 0.10,
                'usg_pct': 0.15, 'ast_to_ratio': 0.10, 'per': 0.15, 'treb_pct': 0.10
            },
            'PF': {
                'efg_pct': 0.10, 'ts_pct': 0.10, 'ast_pct': 0.05, 'tov_pct': 0.10,
                'usg_pct': 0.10, 'ast_to_ratio': 0.05, 'per': 0.15, 'treb_pct': 0.25
            },
            'C': {
                'efg_pct': 0.10, 'ts_pct': 0.10, 'ast_pct': 0.05, 'tov_pct': 0.10,
                'usg_pct': 0.10, 'ast_to_ratio': 0.05, 'per': 0.15, 'treb_pct': 0.25
            }
        }

        # Tier thresholds for player categorization
        self.tier_thresholds = {
            'Elite': 0.85,
            'Starter': 0.70,
            'Role Player': 0.50,
            'Bench Player': 0.30
        }

        self.scaler = StandardScaler()

    def estimate_position(self, df: pd.DataFrame) -> pd.Series:
        """
        Estimate player positions based on statistical profile.

        Args:
            df (pd.DataFrame): DataFrame with player statistics

        Returns:
            pd.Series: Estimated positions
        """
        if df.empty:
            return pd.Series([])

        positions = []

        for _, row in df.iterrows():
            # Simple position estimation based on statistical profile
            ast_rate = row.get('ast_pct', 0)
            reb_rate = row.get('treb_pct', 0)
            usg_rate = row.get('usg_pct', 0)

            if ast_rate > 15 and reb_rate < 8:
                pos = 'PG'
            elif ast_rate > 10 and reb_rate < 10:
                pos = 'SG'
            elif reb_rate > 12 and ast_rate < 8:
                pos = 'C'
            elif reb_rate > 10 and ast_rate < 10:
                pos = 'PF'
            else:
                pos = 'SF'

            positions.append(pos)

        return pd.Series(positions, index=df.index)

    def normalize_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize statistics for fair comparison across different scales.

        Args:
            df (pd.DataFrame): DataFrame with statistics to normalize

        Returns:
            pd.DataFrame: DataFrame with normalized statistics
        """
        if df.empty:
            return df

        # Select columns to normalize
        stat_columns = [
            'efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct',
            'ast_to_ratio', 'per', 'treb_pct', 'oreb_pct', 'dreb_pct'
        ]

        available_cols = [col for col in stat_columns if col in df.columns]

        if not available_cols:
            logger.warning("No statistics available for normalization")
            return df

        # Create normalized DataFrame
        normalized_df = df.copy()

        # Normalize each statistic to 0-1 scale
        for col in available_cols:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val > min_val:
                    normalized_df[f'{col}_norm'] = (df[col] - min_val) / (max_val - min_val)
                else:
                    normalized_df[f'{col}_norm'] = 0.5  # Default to middle if no variation

        return normalized_df

    def calculate_position_adjusted_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate position-adjusted strength scores.

        Args:
            df (pd.DataFrame): DataFrame with normalized statistics and positions

        Returns:
            pd.DataFrame: DataFrame with position-adjusted scores
        """
        if df.empty:
            return df

        result_df = df.copy()
        strength_scores = []

        for _, row in result_df.iterrows():
            position = row.get('position', 'SF')  # Default to SF
            weights = self.position_weights.get(position, self.position_weights['SF'])

            score = 0
            total_weight = 0

            for stat, weight in weights.items():
                norm_stat = f'{stat}_norm'
                if norm_stat in row.index:
                    score += row[norm_stat] * weight
                    total_weight += weight

            # Normalize by total weight
            if total_weight > 0:
                score = score / total_weight
            else:
                score = 0

            strength_scores.append(score)

        result_df['strength_score'] = strength_scores
        return result_df

    def categorize_players(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize players into tiers based on strength scores.

        Args:
            df (pd.DataFrame): DataFrame with strength scores

        Returns:
            pd.DataFrame: DataFrame with player tiers
        """
        if df.empty or 'strength_score' not in df.columns:
            return df

        result_df = df.copy()
        tiers = []

        for _, row in result_df.iterrows():
            score = row['strength_score']

            if score >= self.tier_thresholds['Elite']:
                tier = 'Elite'
            elif score >= self.tier_thresholds['Starter']:
                tier = 'Starter'
            elif score >= self.tier_thresholds['Role Player']:
                tier = 'Role Player'
            elif score >= self.tier_thresholds['Bench Player']:
                tier = 'Bench Player'
            else:
                tier = 'Reserve'

            tiers.append(tier)

        result_df['player_tier'] = tiers
        return result_df

    def identify_strengths_weaknesses(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify player strengths and weaknesses relative to league averages.

        Args:
            df (pd.DataFrame): DataFrame with player statistics

        Returns:
            pd.DataFrame: DataFrame with strength/weakness analysis
        """
        if df.empty:
            return df

        result_df = df.copy()

        # Calculate league averages for key metrics
        key_metrics = ['efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'treb_pct']
        available_metrics = [m for m in key_metrics if m in df.columns]

        if not available_metrics:
            return result_df

        league_averages = {}
        for metric in available_metrics:
            league_averages[metric] = df[metric].mean()

        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []

        for _, row in result_df.iterrows():
            player_strengths = []
            player_weaknesses = []

            for metric in available_metrics:
                player_val = row[metric]
                league_avg = league_averages[metric]

                # Consider it a strength if 10% above average, weakness if 10% below
                threshold = league_avg * 0.1

                if player_val > league_avg + threshold:
                    player_strengths.append(metric)
                elif player_val < league_avg - threshold:
                    player_weaknesses.append(metric)

            strengths.append(', '.join(player_strengths) if player_strengths else 'None')
            weaknesses.append(', '.join(player_weaknesses) if player_weaknesses else 'None')

        result_df['strengths'] = strengths
        result_df['weaknesses'] = weaknesses

        return result_df

    def evaluate_player_strength(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Complete player strength evaluation pipeline.

        Args:
            df (pd.DataFrame): DataFrame with player statistics

        Returns:
            pd.DataFrame: DataFrame with complete strength evaluation
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for strength evaluation")
            return df

        logger.info("Starting player strength evaluation...")

        # Step 1: Estimate positions
        df_with_positions = df.copy()
        df_with_positions['position'] = self.estimate_position(df)

        # Step 2: Normalize statistics
        normalized_df = self.normalize_statistics(df_with_positions)

        # Step 3: Calculate position-adjusted scores
        scored_df = self.calculate_position_adjusted_score(normalized_df)

        # Step 4: Categorize players
        categorized_df = self.categorize_players(scored_df)

        # Step 5: Identify strengths and weaknesses
        final_df = self.identify_strengths_weaknesses(categorized_df)

        # Sort by strength score
        final_df = final_df.sort_values('strength_score', ascending=False)

        logger.info(f"Completed strength evaluation for {len(final_df)} players")
        return final_df

    def get_top_players(self, df: pd.DataFrame, n: int = 10, tier: Optional[str] = None) -> pd.DataFrame:
        """
        Get top players by strength score or tier.

        Args:
            df (pd.DataFrame): DataFrame with strength evaluation
            n (int): Number of top players to return
            tier (str, optional): Filter by specific tier

        Returns:
            pd.DataFrame: Top players DataFrame
        """
        if df.empty:
            return df

        if tier:
            filtered_df = df[df['player_tier'] == tier]
        else:
            filtered_df = df

        return filtered_df.head(n)

    def compare_players(self, df: pd.DataFrame, player_names: List[str]) -> pd.DataFrame:
        """
        Compare specific players side by side.

        Args:
            df (pd.DataFrame): DataFrame with player data
            player_names (List[str]): List of player names to compare

        Returns:
            pd.DataFrame: Comparison DataFrame
        """
        if df.empty:
            return df

        comparison_df = df[df['player'].isin(player_names)].copy()

        if comparison_df.empty:
            logger.warning(f"No players found: {player_names}")
            return comparison_df

        # Select key columns for comparison
        key_columns = [
            'player', 'position', 'strength_score', 'player_tier',
            'efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per',
            'strengths', 'weaknesses'
        ]

        available_columns = [col for col in key_columns if col in comparison_df.columns]

        return comparison_df[available_columns]

    def get_model_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics of the strength evaluation model.

        Args:
            df (pd.DataFrame): DataFrame with strength evaluation

        Returns:
            Dict: Summary statistics
        """
        if df.empty:
            return {}

        summary = {
            'total_players': len(df),
            'tier_distribution': df['player_tier'].value_counts().to_dict(),
            'position_distribution': df['position'].value_counts().to_dict(),
            'strength_score_stats': {
                'mean': df['strength_score'].mean(),
                'median': df['strength_score'].median(),
                'std': df['strength_score'].std(),
                'min': df['strength_score'].min(),
                'max': df['strength_score'].max()
            },
            'top_players': df.head(5)[['player', 'strength_score', 'player_tier']].to_dict('records')
        }

        return summary

def main():
    """Test the player strength evaluation model."""
    from src.data_collection.nba_scraper import NBADataScraper
    from src.analysis.higher_order_stats import HigherOrderStats

    # Load and process sample data
    scraper = NBADataScraper()
    sample_df = scraper.load_sample_data()

    # Calculate higher-order stats
    calculator = HigherOrderStats()
    enhanced_df = calculator.calculate_all_higher_order_stats(sample_df)

    # Evaluate player strength
    model = PlayerStrengthModel()
    evaluated_df = model.evaluate_player_strength(enhanced_df)

    # Display results
    print("Player Strength Evaluation Results:")
    print("=" * 60)

    display_columns = ['player', 'position', 'strength_score', 'player_tier', 'per']
    display_df = evaluated_df[display_columns].round(3)
    print(display_df.to_string(index=False))

    # Show model summary
    summary = model.get_model_summary(evaluated_df)
    print(f"\nModel Summary:")
    print(f"Total Players: {summary['total_players']}")
    print(f"Tier Distribution: {summary['tier_distribution']}")
    print(f"Position Distribution: {summary['position_distribution']}")

    # Save results
    evaluated_df.to_csv("data/processed/nba_player_strength_evaluation.csv", index=False)
    print(f"\nResults saved to data/processed/nba_player_strength_evaluation.csv")

if __name__ == "__main__":
    main()