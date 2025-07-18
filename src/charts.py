import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Optional, Dict


def create_price_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """Create interactive price chart for ETF analysis.

    Parameters
    ----------
    data : pd.DataFrame
        ETF data with 'Close' column and datetime index.
    ticker : str
        Ticker symbol for chart title and labeling.

    Returns
    -------
    go.Figure
        Plotly figure object with interactive price chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name=f'{ticker} Price',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        title=f'{ticker} Price Over Time',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        height=500
    )
    return fig


def create_volume_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """Create interactive volume chart for trading activity analysis.

    Parameters
    ----------
    data : pd.DataFrame
        ETF data with 'Volume' column and datetime index.
    ticker : str
        Ticker symbol for chart title and labeling.

    Returns
    -------
    go.Figure
        Plotly figure object with interactive volume chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Volume'],
        mode='lines',
        name=f'{ticker} Volume',
        line=dict(color='orange', width=2)
    ))

    fig.update_layout(
        title=f'{ticker} Trading Volume Over Time',
        xaxis_title='Date',
        yaxis_title='Volume',
        hovermode='x unified',
        height=500
    )
    return fig


def create_correlation_heatmap(corr_matrix: pd.DataFrame) -> go.Figure:
    """Create correlation heatmap for bond ETF comparison.

    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Correlation matrix with ETF tickers as index and columns.

    Returns
    -------
    go.Figure
        Plotly figure object with correlation heatmap.
    """
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title='Bond ETF Correlation Matrix',
        height=500
    )
    return fig


def create_rolling_volatility_chart(returns: pd.Series, ticker: str, window: int = 30) -> go.Figure:
    """Create rolling volatility chart for risk analysis.

    Parameters
    ----------
    returns : pd.Series
        Daily returns series for the ETF.
    ticker : str
        Ticker symbol for chart title and labeling.
    window : int, optional
        Rolling window size in days. Default is 30.

    Returns
    -------
    go.Figure
        Plotly figure object with rolling volatility chart.
    """
    rolling_vol = returns.rolling(window).std() * np.sqrt(252)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rolling_vol.index,
        y=rolling_vol,
        mode='lines',
        name=f'{ticker} {window}D Volatility',
        line=dict(color='darkred', width=2)
    ))

    fig.update_layout(
        title=f'{ticker} {window}-Day Rolling Volatility (Annualized)',
        xaxis_title='Date',
        yaxis_title='Annualized Volatility',
        hovermode='x unified',
        height=500
    )
    return fig


def create_price_distribution_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """Create price distribution histogram for analysis.

    Parameters
    ----------
    data : pd.DataFrame
        ETF data with 'Close' column.
    ticker : str
        Ticker symbol for chart title and labeling.

    Returns
    -------
    go.Figure
        Plotly figure object with price distribution histogram.
    """
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data['Close'],
        nbinsx=30,
        name=f'{ticker} Price Distribution',
        marker_color='green',
        opacity=0.7
    ))

    fig.update_layout(
        title=f'{ticker} Price Distribution',
        xaxis_title='Price ($)',
        yaxis_title='Frequency',
        height=500
    )
    return fig


def create_daily_range_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """Create daily price range (High - Low) chart.

    Parameters
    ----------
    data : pd.DataFrame
        ETF data with 'High' and 'Low' columns.
    ticker : str
        Ticker symbol for chart title and labeling.

    Returns
    -------
    go.Figure
        Plotly figure object with daily range chart.
    """
    daily_range = data['High'] - data['Low']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=daily_range,
        mode='lines',
        name=f'{ticker} Daily Range',
        line=dict(color='red', width=1),
        opacity=0.7
    ))

    fig.update_layout(
        title=f'{ticker} Daily Price Range (High - Low)',
        xaxis_title='Date',
        yaxis_title='Price Range ($)',
        hovermode='x unified',
        height=500
    )
    return fig


def create_event_overlay_chart(data: pd.DataFrame, ticker: str, events: Dict[str, str]) -> go.Figure:
    """Create price chart with event markers overlay.

    Parameters
    ----------
    data : pd.DataFrame
        ETF data with 'Close' column and datetime index.
    ticker : str
        Ticker symbol for chart title and labeling.
    events : Dict[str, str]
        Dictionary with event dates as keys and event names as values.

    Returns
    -------
    go.Figure
        Plotly figure object with price chart and event markers.
    """
    fig = go.Figure()

    # Add price line
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name=f'{ticker} Price',
        line=dict(color='navy', width=2)
    ))

    # Add event markers
    event_colors = {
        'COVID-19': 'red',
        'Russia Invades Ukraine': 'red',
        'Fed 75bp Hike': 'purple',
        'SVB Collapse': 'orange',
        'EU Green Deal': 'green',
    }

    for date_str, event_name in events.items():
        try:
            event_date = pd.to_datetime(date_str).to_pydatetime()
            if event_date >= data.index[0] and event_date <= data.index[-1]:
                color = event_colors.get(event_name, 'gray')
                fig.add_vline(
                    x=event_date,
                    line=dict(color=color, width=3, dash='dash'),
                    annotation_text=event_name,
                    annotation_position="top"
                )
        except:
            continue

    fig.update_layout(
        title=f'{ticker} Price with Key Events',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        height=600
    )
    return fig


def create_normalized_comparison_chart(data_dict: Dict[str, pd.DataFrame],
                                       title: str = "Normalized Price Comparison") -> go.Figure:
    """Create normalized price comparison chart for multiple ETFs.

    Parameters
    ----------
    data_dict : Dict[str, pd.DataFrame]
        Dictionary with ticker symbols as keys and DataFrames as values.
    title : str, optional
        Chart title. Default is "Normalized Price Comparison".

    Returns
    -------
    go.Figure
        Plotly figure object with normalized price comparison.
    """
    fig = go.Figure()

    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']

    for i, (ticker, data) in enumerate(data_dict.items()):
        if not data.empty and 'Close' in data.columns:
            normalized = data['Close'] / data['Close'].iloc[0]
            color = colors[i % len(colors)]

            fig.add_trace(go.Scatter(
                x=data.index,
                y=normalized,
                mode='lines',
                name=ticker,
                line=dict(color=color, width=2)
            ))

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Normalized Price (Base = 1.0)',
        hovermode='x unified',
        height=500
    )
    return fig


def create_rolling_correlation_chart(correlations: pd.Series, etf_ticker: str, benchmark_ticker: str,
                                     window: int = 252) -> go.Figure:
    """Create rolling correlation chart between ETF and benchmark.

    Parameters
    ----------
    correlations : pd.Series
        Rolling correlation series with datetime index.
    etf_ticker : str
        Target ETF ticker symbol.
    benchmark_ticker : str
        Benchmark ETF ticker symbol.
    window : int, optional
        Rolling window size in days. Default is 252.

    Returns
    -------
    go.Figure
        Plotly figure object with rolling correlation chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=correlations.index,
        y=correlations.values,
        mode='lines',
        name=f'{etf_ticker} vs {benchmark_ticker}',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        title=f'{etf_ticker} vs {benchmark_ticker} Rolling Correlation ({window} days)',
        xaxis_title='Date',
        yaxis_title='Correlation',
        hovermode='x unified',
        height=500
    )
    return fig


def create_performance_comparison(metrics_dict: dict, etfs: list) -> go.Figure:
    """Create bar chart comparing key performance metrics across ETFs.

    Parameters
    ----------
    metrics_dict : dict
        Dictionary with ETF tickers as keys and metrics dictionaries as values.
    etfs : list
        List of ETF ticker symbols to compare.

    Returns
    -------
    go.Figure
        Plotly figure object with performance comparison chart.
    """
    fig = go.Figure()

    # Extract Sharpe ratios for comparison
    sharpe_ratios = [metrics_dict[etf]['sharpe_ratio'] for etf in etfs]
    volatilities = [metrics_dict[etf]['annual_volatility'] for etf in etfs]

    fig.add_trace(go.Bar(
        x=etfs,
        y=sharpe_ratios,
        name='Sharpe Ratio',
        yaxis='y'
    ))

    fig.add_trace(go.Bar(
        x=etfs,
        y=volatilities,
        name='Annual Volatility',
        yaxis='y2'
    ))

    fig.update_layout(
        title='ETF Performance Comparison',
        xaxis_title='ETF',
        yaxis=dict(title='Sharpe Ratio', side='left'),
        yaxis2=dict(title='Annual Volatility', side='right', overlaying='y'),
        height=500
    )
    return fig