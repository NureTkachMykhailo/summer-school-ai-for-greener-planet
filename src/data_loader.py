import yfinance as yf
import pandas as pd
import streamlit as st
from typing import List, Dict, Optional


@st.cache_data
def load_etf_data(ticker: str, period: str = "max") -> Optional[pd.DataFrame]:
    """Load ETF data from Yahoo Finance with caching.

    Parameters
    ----------
    ticker : str
        Ticker symbol for the ETF (e.g., 'BGRN', 'ICLN', 'KRBN').
    period : str, optional
        Time period for data retrieval. Default is "max".

    Returns
    -------
    Optional[pd.DataFrame]
        OHLCV data with a DatetimeIndex, or None if download fails.
    """
    try:
        data = yf.download(ticker, period=period, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except Exception as e:
        st.error(f"Error loading {ticker}: {e}")
        return None


@st.cache_data
def load_benchmark_data(benchmarks: list = None) -> Dict[str, pd.DataFrame]:
    """Load benchmark ETF data for comparison analysis.

    Parameters
    ----------
    benchmarks : list, optional
        List of ticker symbols to load. If None, loads default bond benchmarks.

    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary with ticker symbols as keys and DataFrames as values.
    """
    if benchmarks is None:
        benchmarks = ["SPY", "SPLV", "AGG", "LQD", "TLT", "HYG"]

    data = {}
    for ticker in benchmarks:
        try:
            data[ticker] = yf.download(ticker, period="max", progress=False)
        except Exception as e:
            st.warning(f"Could not load {ticker}: {e}")
    return data


def get_etf_benchmarks(etf_ticker: str) -> List[str]:
    """Get appropriate benchmark ETFs for comparison based on ETF type.

    Parameters
    ----------
    etf_ticker : str
        Target ETF ticker symbol.

    Returns
    -------
    List[str]
        List of benchmark ticker symbols for comparison.
    """
    benchmark_mapping = {
        'BGRN': ['AGG', 'LQD', 'TLT', 'HYG'],
        'ICLN': ['SPY', 'QCLN', 'VGT', 'XLI'],
        'KRBN': ['SPY', 'AGG', 'GLD', 'USO']
    }

    return benchmark_mapping.get(etf_ticker, ['SPY', 'AGG'])


def get_etf_info(etf_ticker: str) -> Dict[str, str]:
    """Get descriptive information about ETF.

    Parameters
    ----------
    etf_ticker : str
        ETF ticker symbol.

    Returns
    -------
    Dict[str, str]
        Dictionary containing ETF name, description, and category.
    """
    etf_info = {
        'BGRN': {
            'name': 'iShares Global Green Bond ETF',
            'description': 'Tracks green bonds worldwide',
            'category': 'Green Bonds'
        },
        'ICLN': {
            'name': 'iShares Global Clean Energy ETF',
            'description': 'Focuses on clean energy companies',
            'category': 'Clean Energy Equity'
        },
        'KRBN': {
            'name': 'KraneShares Global Carbon Strategy ETF',
            'description': 'Carbon allowances and credits',
            'category': 'Carbon Markets'
        }
    }

    return etf_info.get(etf_ticker, {
        'name': etf_ticker,
        'description': 'ETF analysis',
        'category': 'Unknown'
    })