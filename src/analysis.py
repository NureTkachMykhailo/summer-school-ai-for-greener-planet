import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict
from hurst import compute_Hc


def calculate_liquidity_metrics(returns: pd.Series, volume: pd.Series) -> Dict[str, float]:
    """Calculate comprehensive liquidity and trading activity metrics.

    Parameters
    ----------
    returns : pd.Series
        Daily returns series for the ETF.
    volume : pd.Series
        Daily trading volume series for the ETF.

    Returns
    -------
    Dict[str, float]
        Dictionary containing liquidity metrics:

        - avg_daily_volume: Average daily trading volume
        - volume_volatility: Coefficient of variation for volume
        - amihud_illiquidity: Amihud illiquidity ratio
        - zero_return_pct: Percentage of days with zero returns
        - volume_trend: Daily volume trend coefficient
    """
    amihud_illiquidity = (abs(returns) / volume * 1e6)
    avg_illiquidity = amihud_illiquidity.mean()

    avg_daily_volume = volume.mean()
    volume_volatility = volume.std() / volume.mean()

    zero_return_days = (abs(returns) < 0.001).sum()
    zero_return_pct = zero_return_days / len(returns) * 100

    volume_trend = np.polyfit(range(len(volume)), volume, 1)[0]

    return {
        'avg_daily_volume': avg_daily_volume,
        'volume_volatility': volume_volatility,
        'amihud_illiquidity': avg_illiquidity,
        'zero_return_pct': zero_return_pct,
        'volume_trend': volume_trend
    }


def calculate_performance_metrics(returns: pd.Series) -> Dict[str, float]:
    """Calculate comprehensive risk and performance metrics for ETF analysis.

    Parameters
    ----------
    returns : pd.Series
        Daily returns series for the ETF.

    Returns
    -------
    Dict[str, float]
        Dictionary containing performance metrics:

        - annual_volatility: Annualized volatility
        - annual_return: Annualized return
        - sharpe_ratio: Risk-adjusted return ratio
        - skewness: Distribution skewness
        - kurtosis: Distribution kurtosis
        - var_5: 5% Value at Risk
        - cvar_5: 5% Conditional Value at Risk
        - max_drawdown: Maximum drawdown from peak
    """
    return {
        'annual_volatility': returns.std() * np.sqrt(252),
        'annual_return': returns.mean() * 252,
        'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(252),
        'skewness': stats.skew(returns),
        'kurtosis': stats.kurtosis(returns),
        'var_5': returns.quantile(0.05),
        'cvar_5': returns[returns <= returns.quantile(0.05)].mean(),
        'max_drawdown': (returns.cumsum() - returns.cumsum().expanding().max()).min()
    }


def calculate_correlation_matrix(bond_returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate Kendall correlation matrix for bond ETF returns comparison.

    Parameters
    ----------
    bond_returns : pd.DataFrame
        DataFrame with bond ETF daily returns as columns (tickers as column names).

    Returns
    -------
    pd.DataFrame
        Kendall correlation matrix with ETF tickers as index and columns.
    """
    return bond_returns.corr(method='kendall')


def calculate_hurst_exponent(returns: pd.Series) -> tuple:
    """Calculate Hurst exponent for time series analysis.

    Parameters
    ----------
    returns : pd.Series
        Daily returns series for the ETF.

    Returns
    -------
    tuple
        Tuple containing (hurst_value, classification_string).
    """
    hurst_val, _, _ = compute_Hc(returns.values)

    if hurst_val > 0.55:
        classification = "TRENDING / PERSISTENT behavior"
    elif hurst_val < 0.45:
        classification = "MEAN-REVERTING behavior"
    else:
        classification = "RANDOM WALK behavior"

    return hurst_val, classification


def calculate_rolling_correlations(etf_returns: pd.Series, benchmark_returns: pd.Series,
                                   window: int = 252) -> pd.Series:
    """Calculate rolling correlation between ETF and benchmark.

    Parameters
    ----------
    etf_returns : pd.Series
        Daily returns for the target ETF.
    benchmark_returns : pd.Series
        Daily returns for the benchmark ETF.
    window : int, optional
        Rolling window size in days. Default is 252 (1 year).

    Returns
    -------
    pd.Series
        Rolling correlation series with datetime index.
    """
    return etf_returns.rolling(window).corr(benchmark_returns)


def analyze_event_impact(data: pd.DataFrame, events: Dict[str, str]) -> Dict[str, dict]:
    """Analyze price impact around key market events.

    Parameters
    ----------
    data : pd.DataFrame
        ETF data with 'Close' column and datetime index.
    events : dict
        Dictionary with event dates as keys and event names as values.

    Returns
    -------
    Dict[str, dict]
        Dictionary containing event impact analysis for each event.
    """
    event_analysis = {}

    for date_str, event_name in events.items():
        try:
            event_date = pd.to_datetime(date_str)

            # Check if event date is in data range
            if event_date >= data.index[0] and event_date <= data.index[-1]:
                # Get price 5 days before and after
                start_date = event_date - pd.Timedelta(days=10)
                end_date = event_date + pd.Timedelta(days=10)

                event_data = data[start_date:end_date]['Close']

                if len(event_data) > 0:
                    pre_event_price = event_data.iloc[0] if len(event_data) > 0 else None
                    post_event_price = event_data.iloc[-1] if len(event_data) > 0 else None

                    if pre_event_price and post_event_price:
                        impact = (post_event_price - pre_event_price) / pre_event_price * 100
                        event_analysis[event_name] = {
                            'date': event_date,
                            'impact_pct': impact,
                            'pre_price': pre_event_price,
                            'post_price': post_event_price
                        }
        except Exception as e:
            continue

    return event_analysis


def get_market_events() -> Dict[str, str]:
    """Get predefined market events for analysis.

    Returns
    -------
    Dict[str, str]
        Dictionary with event dates as keys and event names as values.
    """
    return {
        '2020-03-12': 'COVID-19',
        '2022-02-24': 'Russia Invades Ukraine',
        '2022-06-15': 'Fed 75bp Hike',
        '2023-03-10': 'SVB Collapse',
        '2019-12-11': 'EU Green Deal',
    }


def compare_volatility_to_benchmarks(etf_vol: float, spy_vol: float, splv_vol: float, ticker: str) -> Dict[str, str]:
    """Compare ETF volatility to market benchmarks with interpretation.

    Parameters
    ----------
    etf_vol : float
        Annual volatility of the target ETF.
    spy_vol : float
        Annual volatility of SPY (S&P 500).
    splv_vol : float
        Annual volatility of SPLV (S&P 500 Low Vol).
    ticker : str
        Ticker symbol of the target ETF.

    Returns
    -------
    Dict[str, str]
        Dictionary containing volatility comparisons and interpretations.
    """
    spy_ratio = etf_vol / spy_vol
    splv_ratio = etf_vol / splv_vol

    interpretations = {}

    if spy_ratio < 0.3:
        interpretations['vs_spy'] = f"{ticker} is {spy_ratio:.2f}x SPY volatility - extremely low risk"
    elif spy_ratio < 0.7:
        interpretations['vs_spy'] = f"{ticker} is {spy_ratio:.2f}x SPY volatility - low risk"
    elif spy_ratio < 1.2:
        interpretations['vs_spy'] = f"{ticker} is {spy_ratio:.2f}x SPY volatility - moderate risk"
    else:
        interpretations['vs_spy'] = f"{ticker} is {spy_ratio:.2f}x SPY volatility - high risk"

    interpretations['vs_splv'] = f"{ticker} vs SPLV: {splv_ratio:.2f}x the volatility"
    interpretations['numerical'] = {
        'spy_ratio': spy_ratio,
        'splv_ratio': splv_ratio
    }

    return interpretations


def interpret_liquidity_status(amihud_ratio: float, zero_return_pct: float, volume_trend: float) -> str:
    """Interpret liquidity metrics and provide market status assessment.

    Parameters
    ----------
    amihud_ratio : float
        Amihud illiquidity ratio.
    zero_return_pct : float
        Percentage of days with zero returns.
    volume_trend : float
        Daily volume trend coefficient.

    Returns
    -------
    str
        Human-readable interpretation of market liquidity status.
    """
    status_parts = []

    # Illiquidity assessment
    if amihud_ratio > 1:
        status_parts.append("🔴 High illiquidity - niche market characteristics")
    elif amihud_ratio > 0.1:
        status_parts.append("🟡 Moderate illiquidity - transitioning market")
    else:
        status_parts.append("🟢 Low illiquidity - mainstream market characteristics")

    # Zero return days assessment
    if zero_return_pct > 5:
        status_parts.append("High inactive trading days - limited institutional participation")
    elif zero_return_pct > 2:
        status_parts.append("Moderate inactive days - growing but not mainstream")
    else:
        status_parts.append("Low inactive days - active institutional market")

    # Volume trend assessment
    if volume_trend > 0:
        status_parts.append(f"📈 Increasing volume trend - market mainstreaming (+{volume_trend:,.0f}/day)")
    else:
        status_parts.append(f"📉 Decreasing volume trend - market consolidation ({volume_trend:,.0f}/day)")

    return "\n".join(status_parts)


def calculate_common_period_data(etf_data: pd.DataFrame, benchmark_data: Dict[str, pd.DataFrame]) -> tuple:
    """Calculate common time period across all datasets for fair comparison.

    Parameters
    ----------
    etf_data : pd.DataFrame
        Primary ETF data with datetime index.
    benchmark_data : Dict[str, pd.DataFrame]
        Dictionary of benchmark ETF data.

    Returns
    -------
    tuple
        Tuple containing (common_start_date, common_end_date, aligned_data_dict).
    """
    # Find common date range
    start_dates = [etf_data.index[0]]
    end_dates = [etf_data.index[-1]]

    for data in benchmark_data.values():
        if not data.empty:
            start_dates.append(data.index[0])
            end_dates.append(data.index[-1])

    common_start = max(start_dates)
    common_end = min(end_dates)

    # Align all data to common period
    aligned_data = {'primary_etf': etf_data[common_start:common_end]}

    for ticker, data in benchmark_data.items():
        if not data.empty:
            aligned_data[ticker] = data[common_start:common_end]

    return common_start, common_end, aligned_data