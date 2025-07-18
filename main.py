# main.py
import streamlit as st
import pandas as pd
import numpy as np

# Import our custom modules
from src.data_loader import load_etf_data, load_benchmark_data, get_etf_benchmarks, get_etf_info
from src.analysis import (calculate_liquidity_metrics, calculate_performance_metrics,
                          calculate_correlation_matrix, calculate_hurst_exponent,
                          get_market_events, analyze_event_impact, interpret_liquidity_status)
from src.charts import (create_price_chart, create_volume_chart, create_correlation_heatmap,
                        create_rolling_volatility_chart, create_price_distribution_chart,
                        create_daily_range_chart, create_event_overlay_chart)

# Page configuration
st.set_page_config(
    page_title="Green ETF Analysis Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Main title
st.title("🌱 Green ETF Analysis Dashboard")
st.markdown("Interactive analysis of green and sustainable investment ETFs")

# Sidebar for ETF selection
st.sidebar.header("ETF Selection")
etf_choice = st.sidebar.selectbox(
    "Choose ETF for Analysis",
    ["BGRN", "ICLN", "KRBN"],
    help="Select an ETF to analyze in detail"
)

# Get ETF information
etf_info = get_etf_info(etf_choice)
st.sidebar.info(f"**{etf_info['name']}** - {etf_info['description']}")
st.sidebar.caption(f"Category: {etf_info['category']}")

# Get appropriate benchmarks for this ETF
benchmarks = get_etf_benchmarks(etf_choice)

# Show benchmark information
st.sidebar.subheader("Benchmark ETFs")
benchmark_info = {
    'SPY': 'S&P 500',
    'SPLV': 'S&P 500 Low Volatility',
    'AGG': 'Total Bond Market',
    'LQD': 'Investment Grade Corporate',
    'TLT': 'Long-Term Treasury',
    'HYG': 'High Yield Corporate',
    'QCLN': 'NASDAQ Clean Energy',
    'VGT': 'Vanguard Technology',
    'XLI': 'SPDR Industrial',
    'GLD': 'Gold ETF',
    'USO': 'Oil ETF'
}

for benchmark in benchmarks:
    st.sidebar.caption(f"• {benchmark}: {benchmark_info.get(benchmark, 'Market Index')}")

# Load data with spinner
with st.spinner(f"Loading {etf_choice} data..."):
    etf_data = load_etf_data(etf_choice)

if etf_data is not None:
    # Calculate basic metrics
    returns = etf_data['Close'].pct_change().dropna()

    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Performance", "⚖️ Risk Analysis", "🔗 Correlations"])

    with tab1:
        st.header(f"{etf_choice} Overview")

        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            current_price = etf_data['Close'].iloc[-1]
            st.metric("Current Price", f"${current_price:.2f}")

        with col2:
            total_return = (etf_data['Close'].iloc[-1] / etf_data['Close'].iloc[0] - 1) * 100
            st.metric("Total Return", f"{total_return:.1f}%")

        with col3:
            annual_vol = returns.std() * np.sqrt(252) * 100
            st.metric("Annual Volatility", f"{annual_vol:.1f}%")

        with col4:
            avg_volume = etf_data['Volume'].mean()
            st.metric("Avg Daily Volume", f"{avg_volume:,.0f}")

        # Price and volume charts
        col1, col2 = st.columns(2)

        with col1:
            price_fig = create_price_chart(etf_data, etf_choice)
            st.plotly_chart(price_fig, use_container_width=True)

        with col2:
            volume_fig = create_volume_chart(etf_data, etf_choice)
            st.plotly_chart(volume_fig, use_container_width=True)

    with tab2:
        st.header(f"{etf_choice} Performance Analysis")

        # Performance metrics
        perf_metrics = calculate_performance_metrics(returns)

        # Display metrics in organized layout
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Return Metrics")
            st.metric("Annual Return", f"{perf_metrics['annual_return']:.2%}")
            st.metric("Sharpe Ratio", f"{perf_metrics['sharpe_ratio']:.2f}")

        with col2:
            st.subheader("Risk Metrics")
            st.metric("Annual Volatility", f"{perf_metrics['annual_volatility']:.2%}")
            st.metric("Max Drawdown", f"{perf_metrics['max_drawdown']:.2%}")

        with col3:
            st.subheader("Distribution")
            st.metric("Skewness", f"{perf_metrics['skewness']:.2f}")
            st.metric("Kurtosis", f"{perf_metrics['kurtosis']:.2f}")

        # Additional analysis charts
        col1, col2 = st.columns(2)

        with col1:
            # Rolling volatility chart
            from src.charts import create_rolling_volatility_chart

            vol_fig = create_rolling_volatility_chart(returns, etf_choice)
            st.plotly_chart(vol_fig, use_container_width=True)

        with col2:
            # Price distribution
            from src.charts import create_price_distribution_chart

            dist_fig = create_price_distribution_chart(etf_data, etf_choice)
            st.plotly_chart(dist_fig, use_container_width=True)

        # Hurst Exponent Analysis
        from src.analysis import calculate_hurst_exponent

        hurst_val, hurst_class = calculate_hurst_exponent(returns)

        st.subheader("Market Behavior Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hurst Exponent", f"{hurst_val:.3f}")
        with col2:
            st.info(f"**Market Behavior:** {hurst_class}")

        # Performance details table
        st.subheader("Detailed Performance Metrics")

        metrics_df = pd.DataFrame([perf_metrics]).T
        metrics_df.columns = ['Value']
        metrics_df['Metric'] = metrics_df.index
        metrics_df = metrics_df[['Metric', 'Value']].reset_index(drop=True)

        st.dataframe(metrics_df, use_container_width=True)

    with tab3:
        st.header(f"{etf_choice} Liquidity & Risk Analysis")

        # Liquidity metrics
        liq_metrics = calculate_liquidity_metrics(returns, etf_data['Volume'])

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Liquidity Metrics")
            st.metric("Average Daily Volume", f"{liq_metrics['avg_daily_volume']:,.0f}")
            st.metric("Volume Volatility (CV)", f"{liq_metrics['volume_volatility']:.2f}")
            st.metric("Zero Return Days", f"{liq_metrics['zero_return_pct']:.1f}%")

        with col2:
            st.subheader("Market Quality")
            st.metric("Amihud Illiquidity", f"{liq_metrics['amihud_illiquidity']:.6f}")

            # Detailed liquidity interpretation
            from src.analysis import interpret_liquidity_status

            liquidity_status = interpret_liquidity_status(
                liq_metrics['amihud_illiquidity'],
                liq_metrics['zero_return_pct'],
                liq_metrics['volume_trend']
            )
            st.text(liquidity_status)

        # Additional risk charts
        col1, col2 = st.columns(2)

        with col1:
            # Daily range analysis
            from src.charts import create_daily_range_chart

            range_fig = create_daily_range_chart(etf_data, etf_choice)
            st.plotly_chart(range_fig, use_container_width=True)

        with col2:
            # Event analysis
            from src.analysis import get_market_events, analyze_event_impact
            from src.charts import create_event_overlay_chart

            events = get_market_events()
            event_fig = create_event_overlay_chart(etf_data, etf_choice, events)
            st.plotly_chart(event_fig, use_container_width=True)

        # Event impact analysis
        st.subheader("Market Event Impact Analysis")
        event_impacts = analyze_event_impact(etf_data, events)

        if event_impacts:
            event_df = pd.DataFrame(event_impacts).T
            event_df = event_df.round(3)
            st.dataframe(event_df, use_container_width=True)
        else:
            st.info("No significant market events occurred during this ETF's trading period.")

    with tab4:
        st.header("Correlation Analysis")

        # Load benchmark data for this specific ETF
        with st.spinner("Loading benchmark data for comparison..."):
            benchmark_data = load_benchmark_data(benchmarks)

        if benchmark_data:
            # Prepare correlation data
            available_benchmarks = {k: v for k, v in benchmark_data.items() if not v.empty}

            if available_benchmarks:
                # Calculate correlations
                all_returns = {}
                all_returns[etf_choice] = returns

                for ticker, data in available_benchmarks.items():
                    if not data.empty:
                        all_returns[ticker] = data['Close'].pct_change().dropna()

                # Align dates
                all_returns = {
                    ticker: (ret.iloc[:, 0] if isinstance(ret, pd.DataFrame) else ret)
                    for ticker, ret in all_returns.items()
                }
                all_returns_df = pd.DataFrame(all_returns).dropna()

                if not all_returns_df.empty:
                    corr_matrix = calculate_correlation_matrix(all_returns_df)

                    # Display correlation heatmap
                    corr_fig = create_correlation_heatmap(corr_matrix)
                    st.plotly_chart(corr_fig, use_container_width=True)

                    # Correlation insights
                    st.subheader("Correlation Insights")

                    if etf_choice in corr_matrix.index:
                        # Find highest correlation
                        correlations = corr_matrix[etf_choice].drop(etf_choice)
                        highest_corr = correlations.abs().idxmax()
                        highest_corr_value = correlations[highest_corr]

                        st.info(f"**{etf_choice}** has the highest correlation with **{highest_corr}** "
                                f"(correlation: {highest_corr_value:.3f})")

                        # Show all correlations in a table
                        st.subheader("Correlation Summary")
                        corr_summary = correlations.sort_values(key=abs, ascending=False)
                        corr_df = pd.DataFrame({
                            'Benchmark': corr_summary.index,
                            'Correlation': corr_summary.values
                        }).reset_index(drop=True)
                        st.dataframe(corr_df, use_container_width=True)

                        # Interpretation based on ETF type
                        if etf_choice == 'BGRN':
                            st.info(
                                "📊 **Bond ETF Analysis**: High correlation with bond indices (AGG, LQD, TLT) suggests integration with traditional fixed income markets.")
                        elif etf_choice == 'ICLN':
                            st.info(
                                "📊 **Clean Energy Analysis**: Correlations with tech (VGT) and industrial (XLI) sectors show sectoral alignment.")
                        elif etf_choice == 'KRBN':
                            st.info(
                                "📊 **Carbon Markets Analysis**: Correlations with commodities (GLD, USO) and bonds (AGG) show unique positioning.")

                else:
                    st.warning("Insufficient overlapping data for correlation analysis")
            else:
                st.warning("No benchmark data available for comparison")
        else:
            st.error("Could not load benchmark data")

else:
    st.error(f"Could not load data for {etf_choice}. Please check your internet connection.")

# Footer
st.markdown("---")
st.markdown("*Data provided by Yahoo Finance. For educational purposes only.*")