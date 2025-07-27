"""
NBA Player Performance Visualizations

This module provides comprehensive visualization capabilities for NBA player analysis,
including exploratory data analysis, player comparisons, and strength evaluations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Dict, List, Optional, Tuple
import logging

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class NBAVisualizations:
    """Comprehensive visualization class for NBA player analysis."""

    def __init__(self):
        # NBA team colors for consistent theming
        self.nba_colors = {
            'LAL': '#552583', 'LAC': '#C8102E', 'GSW': '#1D428A', 'SAC': '#5A2D81',
            'PHX': '#1D1160', 'POR': '#E03A3E', 'DEN': '#0E2240', 'UTA': '#002B5C',
            'MIN': '#0C2340', 'OKC': '#007AC1', 'DAL': '#00538C', 'HOU': '#CE1141',
            'SAS': '#C4CED4', 'MEM': '#5D76A9', 'NOP': '#0C2340', 'MIL': '#00471B',
            'CHI': '#CE1141', 'CLE': '#860038', 'DET': '#C8102E', 'IND': '#002D62',
            'ATL': '#E03A3E', 'MIA': '#98002E', 'ORL': '#0077C0', 'WAS': '#002B5C',
            'BOS': '#007A33', 'PHI': '#006BB6', 'NYK': '#006BB6', 'BKN': '#000000',
            'TOR': '#CE1141', 'CHA': '#1D1160'
        }

        # Position colors
        self.position_colors = {
            'PG': '#FF6B6B', 'SG': '#4ECDC4', 'SF': '#45B7D1',
            'PF': '#96CEB4', 'C': '#FFEAA7'
        }

        # Tier colors
        self.tier_colors = {
            'Elite': '#FF6B6B', 'Starter': '#4ECDC4',
            'Role Player': '#45B7D1', 'Bench Player': '#96CEB4', 'Reserve': '#FFEAA7'
        }

    def create_distribution_plots(self, df: pd.DataFrame, save_path: Optional[str] = None) -> Dict:
        """
        Create distribution plots for key statistics.

        Args:
            df (pd.DataFrame): DataFrame with player statistics
            save_path (str, optional): Path to save plots

        Returns:
            Dict: Dictionary containing plot objects
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for distribution plots")
            return {}

        plots = {}

        # Key statistics to plot
        key_stats = ['efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per']
        available_stats = [stat for stat in key_stats if stat in df.columns]

        if not available_stats:
            logger.warning("No available statistics for distribution plots")
            return {}

        # Create subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()

        for i, stat in enumerate(available_stats):
            if i < len(axes):
                # Histogram with KDE
                sns.histplot(data=df, x=stat, kde=True, ax=axes[i], color='skyblue', alpha=0.7)
                axes[i].set_title(f'Distribution of {stat.upper().replace("_", " ")}')
                axes[i].set_xlabel(stat.upper().replace("_", " "))
                axes[i].set_ylabel('Frequency')

                # Add mean line
                mean_val = df[stat].mean()
                axes[i].axvline(mean_val, color='red', linestyle='--',
                               label=f'Mean: {mean_val:.3f}')
                axes[i].legend()

        # Hide empty subplots
        for i in range(len(available_stats), len(axes)):
            axes[i].set_visible(False)

        plt.tight_layout()
        plots['distribution'] = fig

        if save_path:
            fig.savefig(f"{save_path}/distribution_plots.png", dpi=300, bbox_inches='tight')

        return plots

    def create_correlation_heatmap(self, df: pd.DataFrame, save_path: Optional[str] = None) -> go.Figure:
        """
        Create correlation heatmap for higher-order statistics.

        Args:
            df (pd.DataFrame): DataFrame with player statistics
            save_path (str, optional): Path to save plot

        Returns:
            go.Figure: Plotly figure object
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for correlation heatmap")
            return go.Figure()

        # Select numerical columns for correlation
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        correlation_cols = [col for col in numerical_cols if col in [
            'efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per',
            'treb_pct', 'oreb_pct', 'dreb_pct', 'ast_to_ratio', 'game_score'
        ]]

        if len(correlation_cols) < 2:
            logger.warning("Insufficient numerical columns for correlation analysis")
            return go.Figure()

        # Calculate correlation matrix
        corr_matrix = df[correlation_cols].corr()

        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title="Correlation Matrix of Higher-Order Statistics"
        )

        fig.update_layout(
            width=800,
            height=600,
            title_x=0.5
        )

        if save_path:
            fig.write_html(f"{save_path}/correlation_heatmap.html")

        return fig

    def create_scatter_plots(self, df: pd.DataFrame, save_path: Optional[str] = None) -> Dict:
        """
        Create scatter plots showing relationships between key statistics.

        Args:
            df (pd.DataFrame): DataFrame with player statistics
            save_path (str, optional): Path to save plots

        Returns:
            Dict: Dictionary containing plot objects
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for scatter plots")
            return {}

        plots = {}

        # Key relationships to explore
        relationships = [
            ('ts_pct', 'usg_pct', 'Usage vs True Shooting %'),
            ('ast_pct', 'tov_pct', 'Assist % vs Turnover %'),
            ('efg_pct', 'per', 'Effective FG% vs PER'),
            ('usg_pct', 'per', 'Usage % vs PER'),
            ('ast_pct', 'per', 'Assist % vs PER'),
            ('treb_pct', 'per', 'Rebound % vs PER')
        ]

        available_relationships = [
            (x, y, title) for x, y, title in relationships
            if x in df.columns and y in df.columns
        ]

        if not available_relationships:
            logger.warning("No available relationships for scatter plots")
            return {}

        # Create subplots
        n_plots = len(available_relationships)
        cols = 3
        rows = (n_plots + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(18, 6*rows))
        if rows == 1:
            axes = axes.reshape(1, -1)

        for i, (x_col, y_col, title) in enumerate(available_relationships):
            row = i // cols
            col = i % cols

            # Create scatter plot with position colors
            if 'position' in df.columns:
                for pos in df['position'].unique():
                    pos_data = df[df['position'] == pos]
                    axes[row, col].scatter(
                        pos_data[x_col], pos_data[y_col],
                        label=pos, alpha=0.7, s=50
                    )
                axes[row, col].legend()
            else:
                axes[row, col].scatter(df[x_col], df[y_col], alpha=0.7, s=50)

            axes[row, col].set_xlabel(x_col.upper().replace("_", " "))
            axes[row, col].set_ylabel(y_col.upper().replace("_", " "))
            axes[row, col].set_title(title)

            # Add trend line
            z = np.polyfit(df[x_col], df[y_col], 1)
            p = np.poly1d(z)
            axes[row, col].plot(df[x_col], p(df[x_col]), "r--", alpha=0.8)

        # Hide empty subplots
        for i in range(len(available_relationships), rows * cols):
            row = i // cols
            col = i % cols
            axes[row, col].set_visible(False)

        plt.tight_layout()
        plots['scatter'] = fig

        if save_path:
            fig.savefig(f"{save_path}/scatter_plots.png", dpi=300, bbox_inches='tight')

        return plots

    def create_player_comparison_radar(self, df: pd.DataFrame, player_names: List[str],
                                     save_path: Optional[str] = None) -> go.Figure:
        """
        Create radar chart comparing multiple players.

        Args:
            df (pd.DataFrame): DataFrame with player statistics
            player_names (List[str]): List of player names to compare
            save_path (str, optional): Path to save plot

        Returns:
            go.Figure: Plotly radar chart
        """
        if df.empty or not player_names:
            logger.warning("Empty DataFrame or no player names provided")
            return go.Figure()

        # Filter data for selected players
        player_data = df[df['player'].isin(player_names)]

        if player_data.empty:
            logger.warning(f"No data found for players: {player_names}")
            return go.Figure()

        # Select metrics for radar chart
        radar_metrics = ['efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per']
        available_metrics = [m for m in radar_metrics if m in player_data.columns]

        if len(available_metrics) < 3:
            logger.warning("Insufficient metrics for radar chart")
            return go.Figure()

        # Create radar chart
        fig = go.Figure()

        for _, player in player_data.iterrows():
            values = [player[metric] for metric in available_metrics]

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=available_metrics,
                fill='toself',
                name=player['player'],
                line_color=self.position_colors.get(player.get('position', 'SF'), '#666666')
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max([player_data[metric].max() for metric in available_metrics])]
                )),
            showlegend=True,
            title=f"Player Comparison Radar Chart",
            width=800,
            height=600
        )

        if save_path:
            fig.write_html(f"{save_path}/player_radar_chart.html")

        return fig

    def create_strength_score_ranking(self, df: pd.DataFrame, n: int = 20,
                                    save_path: Optional[str] = None) -> go.Figure:
        """
        Create bar chart ranking players by strength score.

        Args:
            df (pd.DataFrame): DataFrame with strength scores
            n (int): Number of top players to show
            save_path (str, optional): Path to save plot

        Returns:
            go.Figure: Plotly bar chart
        """
        if df.empty or 'strength_score' not in df.columns:
            logger.warning("No strength score data available")
            return go.Figure()

        # Get top N players
        top_players = df.nlargest(n, 'strength_score')

        # Create bar chart
        fig = px.bar(
            top_players,
            x='strength_score',
            y='player',
            orientation='h',
            color='player_tier' if 'player_tier' in top_players.columns else None,
            color_discrete_map=self.tier_colors,
            title=f"Top {n} Players by Strength Score"
        )

        fig.update_layout(
            xaxis_title="Strength Score",
            yaxis_title="Player",
            width=800,
            height=max(400, n * 20),
            title_x=0.5
        )

        if save_path:
            fig.write_html(f"{save_path}/strength_score_ranking.html")

        return fig

    def create_tier_distribution(self, df: pd.DataFrame, save_path: Optional[str] = None) -> go.Figure:
        """
        Create pie chart showing distribution of player tiers.

        Args:
            df (pd.DataFrame): DataFrame with player tiers
            save_path (str, optional): Path to save plot

        Returns:
            go.Figure: Plotly pie chart
        """
        if df.empty or 'player_tier' not in df.columns:
            logger.warning("No tier data available")
            return go.Figure()

        tier_counts = df['player_tier'].value_counts()

        fig = px.pie(
            values=tier_counts.values,
            names=tier_counts.index,
            title="Distribution of Player Tiers",
            color_discrete_map=self.tier_colors
        )

        fig.update_layout(
            width=600,
            height=600,
            title_x=0.5
        )

        if save_path:
            fig.write_html(f"{save_path}/tier_distribution.html")

        return fig

    def create_position_comparison(self, df: pd.DataFrame, save_path: Optional[str] = None) -> go.Figure:
        """
        Create box plots comparing statistics across positions.

        Args:
            df (pd.DataFrame): DataFrame with position and statistics
            save_path (str, optional): Path to save plot

        Returns:
            go.Figure: Plotly box plot
        """
        if df.empty or 'position' not in df.columns:
            logger.warning("No position data available")
            return go.Figure()

        # Select key metrics for comparison
        comparison_metrics = ['efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per']
        available_metrics = [m for m in comparison_metrics if m in df.columns]

        if not available_metrics:
            logger.warning("No metrics available for position comparison")
            return go.Figure()

        # Create subplots
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=[metric.upper().replace("_", " ") for metric in available_metrics],
            specs=[[{"type": "box"}, {"type": "box"}, {"type": "box"}],
                   [{"type": "box"}, {"type": "box"}, {"type": "box"}]]
        )

        for i, metric in enumerate(available_metrics):
            row = (i // 3) + 1
            col = (i % 3) + 1

            for position in df['position'].unique():
                pos_data = df[df['position'] == position][metric]

                fig.add_trace(
                    go.Box(
                        y=pos_data,
                        name=position,
                        marker_color=self.position_colors.get(position, '#666666'),
                        showlegend=(i == 0)
                    ),
                    row=row, col=col
                )

        fig.update_layout(
            title="Statistics Comparison by Position",
            width=1200,
            height=800,
            title_x=0.5
        )

        if save_path:
            fig.write_html(f"{save_path}/position_comparison.html")

        return fig

    def create_interactive_dashboard(self, df: pd.DataFrame, save_path: Optional[str] = None) -> go.Figure:
        """
        Create an interactive dashboard with multiple visualizations.

        Args:
            df (pd.DataFrame): DataFrame with player data
            save_path (str, optional): Path to save dashboard

        Returns:
            go.Figure: Plotly dashboard
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for dashboard")
            return go.Figure()

        # Create subplots for dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                "Strength Score Distribution",
                "Top Players by Strength",
                "Position Distribution",
                "Key Statistics Correlation"
            ],
            specs=[[{"type": "histogram"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )

        # 1. Strength Score Distribution
        if 'strength_score' in df.columns:
            fig.add_trace(
                go.Histogram(x=df['strength_score'], name="Strength Score"),
                row=1, col=1
            )

        # 2. Top Players Bar Chart
        if 'strength_score' in df.columns:
            top_players = df.nlargest(10, 'strength_score')
            fig.add_trace(
                go.Bar(
                    x=top_players['player'],
                    y=top_players['strength_score'],
                    name="Top Players"
                ),
                row=1, col=2
            )

        # 3. Position Distribution
        if 'position' in df.columns:
            pos_counts = df['position'].value_counts()
            fig.add_trace(
                go.Pie(
                    values=pos_counts.values,
                    labels=pos_counts.index,
                    name="Positions"
                ),
                row=2, col=1
            )

        # 4. Correlation Scatter
        if 'ts_pct' in df.columns and 'usg_pct' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['ts_pct'],
                    y=df['usg_pct'],
                    mode='markers',
                    name="TS% vs Usage%"
                ),
                row=2, col=2
            )

        fig.update_layout(
            title="NBA Player Analysis Dashboard",
            width=1200,
            height=800,
            title_x=0.5
        )

        if save_path:
            fig.write_html(f"{save_path}/interactive_dashboard.html")

        return fig

    def create_all_visualizations(self, df: pd.DataFrame, save_path: str = "reports/visualizations") -> Dict:
        """
        Create all visualizations for the dataset.

        Args:
            df (pd.DataFrame): DataFrame with player data
            save_path (str): Path to save all visualizations

        Returns:
            Dict: Dictionary containing all plot objects
        """
        import os
        os.makedirs(save_path, exist_ok=True)

        all_plots = {}

        logger.info("Creating distribution plots...")
        all_plots.update(self.create_distribution_plots(df, save_path))

        logger.info("Creating correlation heatmap...")
        all_plots['correlation_heatmap'] = self.create_correlation_heatmap(df, save_path)

        logger.info("Creating scatter plots...")
        all_plots.update(self.create_scatter_plots(df, save_path))

        if 'strength_score' in df.columns:
            logger.info("Creating strength score ranking...")
            all_plots['strength_ranking'] = self.create_strength_score_ranking(df, save_path=save_path)

            logger.info("Creating tier distribution...")
            all_plots['tier_distribution'] = self.create_tier_distribution(df, save_path=save_path)

        if 'position' in df.columns:
            logger.info("Creating position comparison...")
            all_plots['position_comparison'] = self.create_position_comparison(df, save_path=save_path)

        logger.info("Creating interactive dashboard...")
        all_plots['dashboard'] = self.create_interactive_dashboard(df, save_path=save_path)

        logger.info(f"All visualizations saved to {save_path}")
        return all_plots

def main():
    """Test the visualization module."""
    from src.data_collection.nba_scraper import NBADataScraper
    from src.analysis.higher_order_stats import HigherOrderStats
    from src.models.player_strength_model import PlayerStrengthModel

    # Load and process sample data
    scraper = NBADataScraper()
    sample_df = scraper.load_sample_data()

    # Calculate higher-order stats
    calculator = HigherOrderStats()
    enhanced_df = calculator.calculate_all_higher_order_stats(sample_df)

    # Evaluate player strength
    model = PlayerStrengthModel()
    evaluated_df = model.evaluate_player_strength(enhanced_df)

    # Create visualizations
    viz = NBAVisualizations()
    plots = viz.create_all_visualizations(evaluated_df)

    print("Visualizations created successfully!")
    print("Check the 'reports/visualizations' directory for saved plots.")

if __name__ == "__main__":
    main()