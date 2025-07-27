"""
NBA Player Analysis Dashboard

A comprehensive Streamlit dashboard for interactive NBA player analysis,
featuring data exploration, player comparisons, and strength evaluations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_collection.nba_scraper import NBADataScraper
from src.analysis.higher_order_stats import HigherOrderStats
from src.models.player_strength_model import PlayerStrengthModel
from src.visualization.nba_visualizations import NBAVisualizations

# Page configuration
st.set_page_config(
    page_title="NBA Player Analysis Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .player-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process NBA data."""
    try:
        # Try to load processed data first
        if os.path.exists("data/processed/nba_player_strength_evaluation.csv"):
            return pd.read_csv("data/processed/nba_player_strength_evaluation.csv")

        # If not available, generate sample data
        scraper = NBADataScraper()
        sample_df = scraper.load_sample_data()

        calculator = HigherOrderStats()
        enhanced_df = calculator.calculate_all_higher_order_stats(sample_df)

        model = PlayerStrengthModel()
        evaluated_df = model.evaluate_player_strength(enhanced_df)

        # Save for future use
        os.makedirs("data/processed", exist_ok=True)
        evaluated_df.to_csv("data/processed/nba_player_strength_evaluation.csv", index=False)

        return evaluated_df

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def main():
    """Main dashboard function."""

    # Header
    st.markdown('<h1 class="main-header">🏀 NBA Player Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Beyond the Box Score - Advanced Player Performance Analysis")

    # Load data
    with st.spinner("Loading NBA player data..."):
        df = load_data()

    if df.empty:
        st.error("No data available. Please check the data loading process.")
        return

    # Sidebar for filters
    st.sidebar.header("📊 Filters & Controls")

    # Position filter
    positions = ['All'] + list(df['position'].unique()) if 'position' in df.columns else ['All']
    selected_position = st.sidebar.selectbox("Position", positions)

    # Tier filter
    tiers = ['All'] + list(df['player_tier'].unique()) if 'player_tier' in df.columns else ['All']
    selected_tier = st.sidebar.selectbox("Player Tier", tiers)

    # Strength score range
    if 'strength_score' in df.columns:
        min_score = df['strength_score'].min()
        max_score = df['strength_score'].max()
        score_range = st.sidebar.slider(
            "Strength Score Range",
            min_value=float(min_score),
            max_value=float(max_score),
            value=(float(min_score), float(max_score))
        )

    # Apply filters
    filtered_df = df.copy()

    if selected_position != 'All':
        filtered_df = filtered_df[filtered_df['position'] == selected_position]

    if selected_tier != 'All':
        filtered_df = filtered_df[filtered_df['player_tier'] == selected_tier]

    if 'strength_score' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['strength_score'] >= score_range[0]) &
            (filtered_df['strength_score'] <= score_range[1])
        ]

    # Main content
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Players", len(filtered_df))

    with col2:
        if 'strength_score' in filtered_df.columns:
            avg_strength = filtered_df['strength_score'].mean()
            st.metric("Avg Strength Score", f"{avg_strength:.3f}")

    with col3:
        if 'per' in filtered_df.columns:
            avg_per = filtered_df['per'].mean()
            st.metric("Avg PER", f"{avg_per:.1f}")

    with col4:
        if 'ts_pct' in filtered_df.columns:
            avg_ts = filtered_df['ts_pct'].mean()
            st.metric("Avg TS%", f"{avg_ts:.3f}")

    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", "🏆 Player Rankings", "🔍 Player Comparison",
        "📊 Statistics Analysis", "📋 Data Table"
    ])

    with tab1:
        st.header("📈 Overview Dashboard")

        # Create overview visualizations
        col1, col2 = st.columns(2)

        with col1:
            if 'strength_score' in filtered_df.columns:
                fig_hist = px.histogram(
                    filtered_df, x='strength_score',
                    title="Distribution of Strength Scores",
                    nbins=20
                )
                st.plotly_chart(fig_hist, use_container_width=True)

        with col2:
            if 'player_tier' in filtered_df.columns:
                tier_counts = filtered_df['player_tier'].value_counts()
                fig_pie = px.pie(
                    values=tier_counts.values,
                    names=tier_counts.index,
                    title="Player Tier Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        # Position distribution
        if 'position' in filtered_df.columns:
            st.subheader("Position Analysis")
            col1, col2 = st.columns(2)

            with col1:
                pos_counts = filtered_df['position'].value_counts()
                fig_pos = px.bar(
                    x=pos_counts.index,
                    y=pos_counts.values,
                    title="Players by Position"
                )
                st.plotly_chart(fig_pos, use_container_width=True)

            with col2:
                if 'strength_score' in filtered_df.columns:
                    fig_box = px.box(
                        filtered_df, x='position', y='strength_score',
                        title="Strength Scores by Position"
                    )
                    st.plotly_chart(fig_box, use_container_width=True)

    with tab2:
        st.header("🏆 Player Rankings")

        # Top players by strength score
        if 'strength_score' in filtered_df.columns:
            st.subheader("Top Players by Strength Score")

            n_players = st.slider("Number of players to show", 5, 50, 20)
            top_players = filtered_df.nlargest(n_players, 'strength_score')

            fig_ranking = px.bar(
                top_players,
                x='strength_score',
                y='player',
                orientation='h',
                color='player_tier' if 'player_tier' in top_players.columns else None,
                title=f"Top {n_players} Players by Strength Score"
            )
            st.plotly_chart(fig_ranking, use_container_width=True)

            # Display top players table
            st.subheader("Top Players Details")
            display_cols = ['player', 'position', 'strength_score', 'player_tier', 'per', 'ts_pct']
            available_cols = [col for col in display_cols if col in top_players.columns]
            st.dataframe(top_players[available_cols].round(3))

    with tab3:
        st.header("🔍 Player Comparison")

        # Player selection
        player_names = filtered_df['player'].tolist()

        col1, col2 = st.columns(2)

        with col1:
            player1 = st.selectbox("Select Player 1", player_names, index=0)

        with col2:
            player2 = st.selectbox("Select Player 2", player_names, index=min(1, len(player_names)-1))

        if player1 and player2:
            comparison_players = filtered_df[filtered_df['player'].isin([player1, player2])]

            if not comparison_players.empty:
                # Radar chart comparison
                st.subheader("Player Comparison Radar Chart")

                radar_metrics = ['efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per']
                available_metrics = [m for m in radar_metrics if m in comparison_players.columns]

                if len(available_metrics) >= 3:
                    fig_radar = go.Figure()

                    for _, player in comparison_players.iterrows():
                        values = [player[metric] for metric in available_metrics]

                        fig_radar.add_trace(go.Scatterpolar(
                            r=values,
                            theta=available_metrics,
                            fill='toself',
                            name=player['player']
                        ))

                    fig_radar.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                        showlegend=True,
                        title="Player Comparison"
                    )

                    st.plotly_chart(fig_radar, use_container_width=True)

                # Side-by-side comparison table
                st.subheader("Detailed Comparison")
                comparison_cols = [
                    'player', 'position', 'strength_score', 'player_tier',
                    'efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per'
                ]
                available_comparison_cols = [col for col in comparison_cols if col in comparison_players.columns]
                st.dataframe(comparison_players[available_comparison_cols].round(3))

    with tab4:
        st.header("📊 Statistics Analysis")

        # Correlation heatmap
        st.subheader("Correlation Analysis")

        numerical_cols = filtered_df.select_dtypes(include=['number']).columns
        correlation_cols = [col for col in numerical_cols if col in [
            'efg_pct', 'ts_pct', 'ast_pct', 'tov_pct', 'usg_pct', 'per',
            'treb_pct', 'oreb_pct', 'dreb_pct', 'ast_to_ratio', 'game_score'
        ]]

        if len(correlation_cols) >= 2:
            corr_matrix = filtered_df[correlation_cols].corr()

            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title="Correlation Matrix of Higher-Order Statistics"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

        # Scatter plots
        st.subheader("Key Relationships")

        relationships = [
            ('ts_pct', 'usg_pct', 'Usage vs True Shooting %'),
            ('ast_pct', 'tov_pct', 'Assist % vs Turnover %'),
            ('efg_pct', 'per', 'Effective FG% vs PER'),
            ('usg_pct', 'per', 'Usage % vs PER')
        ]

        available_relationships = [
            (x, y, title) for x, y, title in relationships
            if x in filtered_df.columns and y in filtered_df.columns
        ]

        if available_relationships:
            cols = st.columns(2)

            for i, (x_col, y_col, title) in enumerate(available_relationships):
                col_idx = i % 2

                fig_scatter = px.scatter(
                    filtered_df, x=x_col, y=y_col,
                    color='position' if 'position' in filtered_df.columns else None,
                    title=title,
                    hover_data=['player']
                )

                cols[col_idx].plotly_chart(fig_scatter, use_container_width=True)

    with tab5:
        st.header("📋 Data Table")

        # Search functionality
        search_term = st.text_input("Search players by name:")

        if search_term:
            search_df = filtered_df[filtered_df['player'].str.contains(search_term, case=False)]
        else:
            search_df = filtered_df

        # Display data
        st.dataframe(search_df, use_container_width=True)

        # Download button
        csv = search_df.to_csv(index=False)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="nba_player_analysis.csv",
            mime="text/csv"
        )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>NBA Player Analysis Dashboard | Beyond the Box Score</p>
        <p>Advanced analytics and visualizations for NBA player performance evaluation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()