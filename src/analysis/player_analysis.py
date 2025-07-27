"""
Main NBA Player Analysis Pipeline

This script orchestrates the complete NBA player analysis pipeline,
from data collection through higher-order statistics calculation,
player strength evaluation, and visualization generation.
"""

import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Import our modules
from src.data_collection.nba_scraper import NBADataScraper
from src.analysis.higher_order_stats import HigherOrderStats
from src.models.player_strength_model import PlayerStrengthModel
from src.visualization.nba_visualizations import NBAVisualizations

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NBAPlayerAnalysis:
    """Complete NBA player analysis pipeline."""

    def __init__(self, data_dir: str = "data", reports_dir: str = "reports"):
        self.data_dir = data_dir
        self.reports_dir = reports_dir
        self.scraper = NBADataScraper()
        self.calculator = HigherOrderStats()
        self.model = PlayerStrengthModel()
        self.viz = NBAVisualizations()

        # Create directories
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(f"{data_dir}/raw", exist_ok=True)
        os.makedirs(f"{data_dir}/processed", exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(f"{reports_dir}/visualizations", exist_ok=True)

    def collect_data(self, use_sample: bool = True, seasons: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Collect NBA player data.

        Args:
            use_sample (bool): Whether to use sample data or scrape real data
            seasons (List[int], optional): List of seasons to scrape

        Returns:
            pd.DataFrame: Collected player data
        """
        logger.info("Starting data collection...")

        if use_sample:
            logger.info("Using sample data for development...")
            df = self.scraper.load_sample_data()
        else:
            logger.info("Scraping real NBA data...")
            if seasons is None:
                seasons = [2024]  # Default to current season

            season_data = self.scraper.get_multiple_seasons(seasons[0], seasons[-1])
            df = pd.concat(season_data.values(), ignore_index=True) if season_data else pd.DataFrame()

        # Clean the data
        cleaned_df = self.scraper.clean_player_data(df)

        # Save raw data
        cleaned_df.to_csv(f"{self.data_dir}/raw/nba_player_data.csv", index=False)
        logger.info(f"Data collection complete. {len(cleaned_df)} players collected.")

        return cleaned_df

    def calculate_higher_order_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate higher-order statistics from basic box score data.

        Args:
            df (pd.DataFrame): Basic player statistics

        Returns:
            pd.DataFrame: DataFrame with higher-order statistics
        """
        logger.info("Calculating higher-order statistics...")

        enhanced_df = self.calculator.calculate_all_higher_order_stats(df)

        # Save enhanced data
        enhanced_df.to_csv(f"{self.data_dir}/processed/nba_enhanced_stats.csv", index=False)
        logger.info("Higher-order statistics calculation complete.")

        return enhanced_df

    def evaluate_player_strength(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluate player strength using the comprehensive model.

        Args:
            df (pd.DataFrame): DataFrame with higher-order statistics

        Returns:
            pd.DataFrame: DataFrame with strength evaluations
        """
        logger.info("Evaluating player strength...")

        evaluated_df = self.model.evaluate_player_strength(df)

        # Save evaluation results
        evaluated_df.to_csv(f"{self.data_dir}/processed/nba_player_strength_evaluation.csv", index=False)
        logger.info("Player strength evaluation complete.")

        return evaluated_df

    def generate_visualizations(self, df: pd.DataFrame) -> Dict:
        """
        Generate comprehensive visualizations.

        Args:
            df (pd.DataFrame): DataFrame with complete player analysis

        Returns:
            Dict: Dictionary containing all visualization objects
        """
        logger.info("Generating visualizations...")

        viz_path = f"{self.reports_dir}/visualizations"
        plots = self.viz.create_all_visualizations(df, viz_path)

        logger.info("Visualization generation complete.")
        return plots

    def generate_insights_report(self, df: pd.DataFrame) -> str:
        """
        Generate insights report based on the analysis.

        Args:
            df (pd.DataFrame): DataFrame with complete player analysis

        Returns:
            str: Path to the generated report
        """
        logger.info("Generating insights report...")

        report_path = f"{self.reports_dir}/nba_analysis_insights.md"

        with open(report_path, 'w') as f:
            f.write("# NBA Player Performance Analysis - Insights Report\n\n")
            f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write("This report presents a comprehensive analysis of NBA player performance ")
            f.write("using advanced analytics and higher-order statistics. The analysis ")
            f.write("demonstrates how foundational box score data can be leveraged to gain ")
            f.write("deeper insights into player effectiveness and impact.\n\n")

            # Methodology
            f.write("## Methodology\n\n")
            f.write("### Data Collection\n")
            f.write("- Player statistics collected from Basketball-Reference.com\n")
            f.write("- Data cleaned and standardized for analysis\n")
            f.write("- Minimum playing time and games played filters applied\n\n")

            f.write("### Higher-Order Statistics Calculated\n")
            stat_descriptions = self.calculator.get_stat_descriptions()
            for stat, description in stat_descriptions.items():
                f.write(f"- **{stat.upper().replace('_', ' ')}**: {description}\n")
            f.write("\n")

            f.write("### Player Strength Model\n")
            f.write("- Position-adjusted weighting schemes\n")
            f.write("- Normalized statistics for fair comparison\n")
            f.write("- Tier-based categorization (Elite, Starter, Role Player, Bench)\n\n")

            # Key Findings
            f.write("## Key Findings\n\n")

            if not df.empty:
                # Top players
                if 'strength_score' in df.columns:
                    top_players = df.nlargest(5, 'strength_score')
                    f.write("### Top 5 Players by Strength Score\n\n")
                    for i, (_, player) in enumerate(top_players.iterrows(), 1):
                        f.write(f"{i}. **{player['player']}** ({player.get('position', 'N/A')}) - ")
                        f.write(f"Strength Score: {player['strength_score']:.3f}\n")
                    f.write("\n")

                # Tier distribution
                if 'player_tier' in df.columns:
                    tier_counts = df['player_tier'].value_counts()
                    f.write("### Player Tier Distribution\n\n")
                    for tier, count in tier_counts.items():
                        percentage = (count / len(df)) * 100
                        f.write(f"- **{tier}**: {count} players ({percentage:.1f}%)\n")
                    f.write("\n")

                # Position analysis
                if 'position' in df.columns:
                    f.write("### Position Analysis\n\n")
                    pos_stats = df.groupby('position').agg({
                        'strength_score': ['mean', 'std'],
                        'per': ['mean', 'std'],
                        'ts_pct': ['mean', 'std']
                    }).round(3)
                    f.write("Average statistics by position:\n\n")
                    f.write("| Position | Avg Strength Score | Avg PER | Avg TS% |\n")
                    f.write("|----------|-------------------|---------|---------|\n")
                    for pos in df['position'].unique():
                        pos_data = df[df['position'] == pos]
                        avg_strength = pos_data['strength_score'].mean()
                        avg_per = pos_data['per'].mean()
                        avg_ts = pos_data['ts_pct'].mean()
                        f.write(f"| {pos} | {avg_strength:.3f} | {avg_per:.1f} | {avg_ts:.3f} |\n")
                    f.write("\n")

                # Statistical insights
                f.write("### Statistical Insights\n\n")

                if 'ts_pct' in df.columns and 'usg_pct' in df.columns:
                    correlation = df['ts_pct'].corr(df['usg_pct'])
                    f.write(f"- **Usage vs Efficiency**: Correlation between True Shooting % and Usage %: {correlation:.3f}\n")

                if 'ast_pct' in df.columns and 'tov_pct' in df.columns:
                    correlation = df['ast_pct'].corr(df['tov_pct'])
                    f.write(f"- **Playmaking**: Correlation between Assist % and Turnover %: {correlation:.3f}\n")

                if 'efg_pct' in df.columns and 'per' in df.columns:
                    correlation = df['efg_pct'].corr(df['per'])
                    f.write(f"- **Shooting vs Overall Impact**: Correlation between eFG% and PER: {correlation:.3f}\n")
                f.write("\n")

            # Limitations
            f.write("## Limitations\n\n")
            f.write("- Analysis based on box score data only\n")
            f.write("- Simplified position estimation\n")
            f.write("- Limited defensive metrics\n")
            f.write("- Sample size constraints for development\n\n")

            # Future Work
            f.write("## Future Work\n\n")
            f.write("- Incorporate play-by-play data\n")
            f.write("- Add defensive metrics and spatial analytics\n")
            f.write("- Implement machine learning for predictions\n")
            f.write("- Expand to multiple seasons for trend analysis\n")
            f.write("- Include team context and lineup data\n\n")

            # Technical Details
            f.write("## Technical Details\n\n")
            f.write(f"- **Total Players Analyzed**: {len(df)}\n")
            f.write(f"- **Statistics Calculated**: {len(self.calculator.get_stat_descriptions())}\n")
            f.write(f"- **Visualizations Generated**: Multiple interactive and static plots\n")
            f.write(f"- **Analysis Pipeline**: Data Collection → Higher-Order Stats → Strength Evaluation → Visualization\n\n")

        logger.info(f"Insights report generated: {report_path}")
        return report_path

    def run_complete_analysis(self, use_sample: bool = True,
                            generate_viz: bool = True,
                            generate_report: bool = True) -> Dict:
        """
        Run the complete NBA player analysis pipeline.

        Args:
            use_sample (bool): Whether to use sample data
            generate_viz (bool): Whether to generate visualizations
            generate_report (bool): Whether to generate insights report

        Returns:
            Dict: Analysis results and metadata
        """
        logger.info("Starting complete NBA player analysis pipeline...")

        results = {
            'timestamp': datetime.now().isoformat(),
            'use_sample': use_sample,
            'data_collection': {},
            'higher_order_stats': {},
            'strength_evaluation': {},
            'visualizations': {},
            'report': {}
        }

        try:
            # Step 1: Data Collection
            df = self.collect_data(use_sample=use_sample)
            results['data_collection'] = {
                'players_collected': len(df),
                'columns': list(df.columns),
                'data_path': f"{self.data_dir}/raw/nba_player_data.csv"
            }

            # Step 2: Higher-Order Statistics
            enhanced_df = self.calculate_higher_order_stats(df)
            results['higher_order_stats'] = {
                'players_processed': len(enhanced_df),
                'new_columns': [col for col in enhanced_df.columns if col not in df.columns],
                'data_path': f"{self.data_dir}/processed/nba_enhanced_stats.csv"
            }

            # Step 3: Player Strength Evaluation
            evaluated_df = self.evaluate_player_strength(enhanced_df)
            results['strength_evaluation'] = {
                'players_evaluated': len(evaluated_df),
                'tier_distribution': evaluated_df['player_tier'].value_counts().to_dict() if 'player_tier' in evaluated_df.columns else {},
                'position_distribution': evaluated_df['position'].value_counts().to_dict() if 'position' in evaluated_df.columns else {},
                'data_path': f"{self.data_dir}/processed/nba_player_strength_evaluation.csv"
            }

            # Step 4: Visualizations
            if generate_viz:
                plots = self.generate_visualizations(evaluated_df)
                results['visualizations'] = {
                    'plots_generated': len(plots),
                    'plot_types': list(plots.keys()),
                    'viz_path': f"{self.reports_dir}/visualizations"
                }

            # Step 5: Insights Report
            if generate_report:
                report_path = self.generate_insights_report(evaluated_df)
                results['report'] = {
                    'report_path': report_path,
                    'report_generated': True
                }

            logger.info("Complete NBA player analysis pipeline finished successfully!")

        except Exception as e:
            logger.error(f"Error in analysis pipeline: {str(e)}")
            results['error'] = str(e)

        return results

def main():
    """Main function to run the complete analysis."""
    analyzer = NBAPlayerAnalysis()

    print("🏀 NBA Player Performance Analysis - Beyond the Box Score")
    print("=" * 60)

    # Run complete analysis
    results = analyzer.run_complete_analysis(
        use_sample=True,  # Use sample data for development
        generate_viz=True,
        generate_report=True
    )

    # Display results summary
    print("\n📊 Analysis Results Summary:")
    print("-" * 40)

    if 'error' not in results:
        print(f"✅ Data Collection: {results['data_collection']['players_collected']} players")
        print(f"✅ Higher-Order Stats: {len(results['higher_order_stats']['new_columns'])} new metrics")
        print(f"✅ Strength Evaluation: {results['strength_evaluation']['players_evaluated']} players evaluated")

        if results['visualizations']:
            print(f"✅ Visualizations: {results['visualizations']['plots_generated']} plots generated")

        if results['report']['report_generated']:
            print(f"✅ Insights Report: Generated successfully")

        print(f"\n📁 Data saved to: {analyzer.data_dir}")
        print(f"📊 Visualizations saved to: {analyzer.reports_dir}/visualizations")
        print(f"📋 Report saved to: {results['report']['report_path']}")

        # Show top players if available
        if os.path.exists(results['strength_evaluation']['data_path']):
            top_players_df = pd.read_csv(results['strength_evaluation']['data_path'])
            if 'strength_score' in top_players_df.columns:
                print(f"\n🏆 Top 5 Players by Strength Score:")
                top_5 = top_players_df.nlargest(5, 'strength_score')
                for i, (_, player) in enumerate(top_5.iterrows(), 1):
                    print(f"{i}. {player['player']} - {player['strength_score']:.3f}")

    else:
        print(f"❌ Analysis failed: {results['error']}")

if __name__ == "__main__":
    main()