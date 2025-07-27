"""
Test script for NBA Player Analysis System

This script tests all major components of the NBA analysis system
to ensure everything works correctly.
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_data_collection():
    """Test data collection module."""
    print("Testing data collection...")

    try:
        from data_collection.nba_scraper import NBADataScraper

        scraper = NBADataScraper()
        sample_df = scraper.load_sample_data()

        print(f"✅ Data collection successful: {len(sample_df)} players loaded")
        print(f"   Columns: {list(sample_df.columns)}")

        # Test data cleaning
        cleaned_df = scraper.clean_player_data(sample_df)
        print(f"✅ Data cleaning successful: {len(cleaned_df)} players after cleaning")

        return cleaned_df

    except Exception as e:
        print(f"❌ Data collection failed: {str(e)}")
        return None

def test_higher_order_stats(df):
    """Test higher-order statistics calculation."""
    print("\nTesting higher-order statistics...")

    try:
        from analysis.higher_order_stats import HigherOrderStats

        calculator = HigherOrderStats()
        enhanced_df = calculator.calculate_all_higher_order_stats(df)

        # Check for new columns
        original_cols = set(df.columns)
        enhanced_cols = set(enhanced_df.columns)
        new_cols = enhanced_cols - original_cols

        print(f"✅ Higher-order stats successful: {len(new_cols)} new metrics calculated")
        print(f"   New metrics: {list(new_cols)}")

        return enhanced_df

    except Exception as e:
        print(f"❌ Higher-order stats failed: {str(e)}")
        return None

def test_player_strength_model(df):
    """Test player strength evaluation model."""
    print("\nTesting player strength model...")

    try:
        from models.player_strength_model import PlayerStrengthModel

        model = PlayerStrengthModel()
        evaluated_df = model.evaluate_player_strength(df)

        # Check for strength score and tier
        has_strength = 'strength_score' in evaluated_df.columns
        has_tier = 'player_tier' in evaluated_df.columns
        has_position = 'position' in evaluated_df.columns

        print(f"✅ Player strength model successful:")
        print(f"   - Strength scores: {has_strength}")
        print(f"   - Player tiers: {has_tier}")
        print(f"   - Position estimates: {has_position}")

        if has_strength:
            print(f"   - Strength score range: {evaluated_df['strength_score'].min():.3f} to {evaluated_df['strength_score'].max():.3f}")

        return evaluated_df

    except Exception as e:
        print(f"❌ Player strength model failed: {str(e)}")
        return None

def test_visualizations(df):
    """Test visualization module."""
    print("\nTesting visualizations...")

    try:
        from visualization.nba_visualizations import NBAVisualizations

        viz = NBAVisualizations()

        # Test basic visualization creation
        plots = viz.create_all_visualizations(df, save_path="test_viz")

        print(f"✅ Visualizations successful: {len(plots)} plots created")
        print(f"   Plot types: {list(plots.keys())}")

        return True

    except Exception as e:
        print(f"❌ Visualizations failed: {str(e)}")
        return False

def test_dashboard():
    """Test dashboard functionality."""
    print("\nTesting dashboard...")

    try:
        # Test if dashboard can be imported
        import streamlit as st
        print("✅ Streamlit available for dashboard")

        # Test dashboard script
        dashboard_path = "dashboards/main_dashboard.py"
        if os.path.exists(dashboard_path):
            print("✅ Dashboard script exists")
            return True
        else:
            print("❌ Dashboard script not found")
            return False

    except ImportError:
        print("❌ Streamlit not available for dashboard")
        return False
    except Exception as e:
        print(f"❌ Dashboard test failed: {str(e)}")
        return False

def test_complete_pipeline():
    """Test the complete analysis pipeline."""
    print("\nTesting complete pipeline...")

    try:
        from analysis.player_analysis import NBAPlayerAnalysis

        analyzer = NBAPlayerAnalysis()
        results = analyzer.run_complete_analysis(
            use_sample=True,
            generate_viz=False,  # Skip viz for faster testing
            generate_report=False  # Skip report for faster testing
        )

        if 'error' not in results:
            print("✅ Complete pipeline successful")
            print(f"   - Players collected: {results['data_collection']['players_collected']}")
            print(f"   - New metrics: {len(results['higher_order_stats']['new_columns'])}")
            print(f"   - Players evaluated: {results['strength_evaluation']['players_evaluated']}")
            return True
        else:
            print(f"❌ Complete pipeline failed: {results['error']}")
            return False

    except Exception as e:
        print(f"❌ Complete pipeline failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🏀 NBA Player Analysis System - Test Suite")
    print("=" * 50)

    # Test individual components
    df = test_data_collection()
    if df is None:
        print("\n❌ System test failed at data collection stage")
        return

    enhanced_df = test_higher_order_stats(df)
    if enhanced_df is None:
        print("\n❌ System test failed at higher-order stats stage")
        return

    evaluated_df = test_player_strength_model(enhanced_df)
    if evaluated_df is None:
        print("\n❌ System test failed at player strength model stage")
        return

    viz_success = test_visualizations(evaluated_df)
    dashboard_success = test_dashboard()

    pipeline_success = test_complete_pipeline()

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    tests = [
        ("Data Collection", df is not None),
        ("Higher-Order Stats", enhanced_df is not None),
        ("Player Strength Model", evaluated_df is not None),
        ("Visualizations", viz_success),
        ("Dashboard", dashboard_success),
        ("Complete Pipeline", pipeline_success)
    ]

    passed = 0
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if success:
            passed += 1

    print(f"\nOverall: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("\n🎉 All tests passed! The NBA analysis system is ready to use.")
        print("\nNext steps:")
        print("1. Run: python src/analysis/player_analysis.py")
        print("2. Launch dashboard: streamlit run dashboards/main_dashboard.py")
        print("3. Explore notebooks in the notebooks/ directory")
    else:
        print(f"\n⚠️  {len(tests) - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()