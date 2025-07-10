# Green Assets Market Evolution Analysis

A comprehensive quantitative analysis of three distinct green finance instruments: carbon allowances (KRBN), clean energy equities (ICLN), and green bonds (BGRN). This study examines their evolution from niche environmental tools to institutional investment products, with particular focus on market maturation, liquidity dynamics, and diversification characteristics.

## 🎯 Key Findings

- **KRBN (Carbon Allowances)**: Successfully achieved institutional accessibility while preserving environmental independence and exceptional diversification benefits
- **ICLN (Clean Energy Equities)**: Mainstream adoption with complete integration into traditional equity markets, losing environmental distinctiveness  
- **BGRN (Green Bonds)**: Failed differentiation from traditional bonds despite "green" labeling, offering minimal investment value

## 📊 Analysis Overview

### Market Evolution Assessment
Each asset demonstrates distinct scaling patterns over 5-17 year periods:

| Asset | Time Period | Market Status | Key Characteristic |
|-------|-------------|---------------|-------------------|
| KRBN | 2020-2025 | Institutional Diversifier | Policy-responsive, crisis hedge |
| ICLN | 2008-2025 | Mainstream Equity Sector | High correlation, retail-driven |
| BGRN | 2018-2025 | Redundant Bond Product | Minimal differentiation |

### Liquidity & Market Maturation
- **KRBN**: 96% illiquidity improvement, 346% volume growth - successful scaling
- **ICLN**: 96% illiquidity improvement, 11,063% volume growth - complete mainstream adoption  
- **BGRN**: 92% illiquidity improvement, but declining volumes - institutional disinterest

### Diversification Analysis
Correlation analysis reveals dramatically different integration levels:

- **KRBN**: Near-zero correlations (0.02-0.22) with traditional assets - exceptional diversification
- **ICLN**: High correlations (0.65-0.91) with equity markets - minimal diversification  
- **BGRN**: 0.84 correlation with aggregate bonds (AGG) - no diversification value

## 📁 Repository Structure

```
├── project_data/
│   ├── allowances/          # Carbon allowances data (KRBN, etc.)
│   ├── bonds/              # Green bonds data (BGRN, AGG, etc.)  
│   └── stocks/             # Clean energy equities (ICLN, etc.)
├── plots/
│   ├── krbn/              # KRBN analysis visualizations
│   ├── icln/              # ICLN analysis visualizations
│   └── bgrn/              # BGRN analysis visualizations
├── notebooks/
│   ├── krbn-analysis.ipynb    # Carbon allowances analysis
│   ├── icln-analysis.ipynb    # Clean energy analysis
│   └── bgrn-analysis.ipynb    # Green bonds analysis
└── README.md
```

## 🛠️ Methodology

### Data Sources
- **Price & Volume Data**: Yahoo Finance API via `yfinance`
- **Analysis Period**: Asset-specific periods matching market availability
- **Benchmark Assets**: SPY, AGG, GLD, USO for correlation analysis

### Key Metrics
- **Liquidity**: Amihud illiquidity ratio, zero-return days, volume trends
- **Risk-Return**: Volatility, Sharpe ratios, maximum drawdowns
- **Market Behavior**: Hurst exponents, rolling correlations, crisis response
- **Diversification**: Static and time-varying correlation analysis

### Statistical Methods
- Peak detection for volatility clustering analysis
- Rolling window correlation (252-day) for time-varying relationships
- Hurst exponent calculation for mean-reversion vs momentum characteristics
- Event study methodology for crisis response analysis

## 📈 Key Visualizations

### Market Maturation Analysis
- **Illiquidity Evolution**: Dramatic improvement patterns showing institutional adoption
- **Volume Growth**: Exponential scaling vs. declining interest patterns
- **Price Distribution**: Bimodal vs. normal distributions revealing structural breaks

### Risk-Return Characteristics  
- **Volatility Clustering**: GARCH effects and crisis sensitivity
- **Correlation Matrices**: Asset interdependence and portfolio implications
- **Performance Comparison**: Risk-adjusted returns across asset classes

### Crisis Response Patterns
- **Event Correlation**: Response to Russia-Ukraine, COVID-19, banking crises
- **Policy Sensitivity**: Reactions to green policy vs. financial market events
- **Hedging Effectiveness**: Crisis protection vs. normal period diversification

## 🎓 Academic Contributions

### Novel Insights
1. **Three-Phase Evolution Model**: Niche → Institutional Discovery → Mainstream Integration
2. **Diversification Paradox**: How mainstream success can eliminate environmental benefits
3. **Crisis Hedge Validation**: Carbon allowances as effective portfolio protection during stress

### Policy Implications
- Carbon markets demonstrate successful environmental finance scaling
- Green bonds require structural reform to provide genuine differentiation
- Clean energy equities show tension between financial and environmental objectives

## 📋 Requirements

### Python Environment
```python
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
yfinance>=0.1.70
scipy>=1.7.0
```

### Installation
```bash
git clone https://github.com/NureTkachMykhailo/green-assets-analysis
cd green-assets-analysis
pip install -r requirements.txt
```

## 🚀 Usage

### Quick Start
```python
# Load and analyze KRBN data
import yfinance as yf
import pandas as pd

# Download KRBN data
krbn = yf.download("KRBN", period="max")

# Run liquidity analysis
from analysis.liquidity import calculate_amihud_ratio
illiquidity = calculate_amihud_ratio(krbn)
```

### Reproducing Analysis
1. **Data Collection**: Run data download scripts for each asset class
2. **Individual Analysis**: Execute asset-specific Jupyter notebooks  
3. **Comparative Analysis**: Run cross-asset correlation and performance studies
4. **Visualization**: Generate publication-ready plots and charts

## 📊 Results Summary

### Portfolio Implications
- **Recommended**: KRBN for diversification and crisis hedging (5-10% allocation)
- **Conditional**: ICLN for sector exposure if accepting high correlation risk
- **Avoid**: BGRN offers no benefits over traditional bond alternatives (AGG)

### Investment Thesis Validation
The analysis confirms that **not all green finance scaling is beneficial** - preserving environmental asset distinctiveness requires careful market design rather than unrestricted financial market integration.

## 🔬 Future Research

### Potential Extensions
- **Expanded Universe**: Additional green assets (renewable energy infrastructure, ESG ETFs)
- **International Markets**: European and Asian green finance instruments
- **Behavioral Analysis**: Google Trends correlation with institutional flows
- **Policy Impact**: Quantitative assessment of regulatory changes on market dynamics

### Methodological Improvements
- **Machine Learning**: Alternative risk factor models for green assets
- **High-Frequency**: Intraday liquidity and volatility analysis
- **Options Markets**: Implied volatility and risk premium analysis

## 📚 References

### Academic Literature
- Riedl, A., & Smeets, P. (2017). Why do investors hold socially responsible mutual funds? *Journal of Finance*, 72(6), 2505-2550.
- Ehlers, T., & Packer, F. (2017). Green bond finance and certification. *BIS Quarterly Review*, September, 89-104.

### Data Sources
- Yahoo Finance for historical price and volume data
- BlackRock iShares for ETF methodology and holdings information
- European Environment Agency for carbon market regulatory information

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📧 Contact

**Author**: Mykhailo Tkach  
**Email**: mykhailo.tkach@nure.ua  
**LinkedIn**: 

---

*This analysis is for educational and research purposes only and should not be considered as investment advice. Past performance does not guarantee future results.*