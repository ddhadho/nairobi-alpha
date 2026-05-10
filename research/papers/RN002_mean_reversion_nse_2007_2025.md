# Nairobi Alpha — Research Note 002
## Cross-Sectional Mean Reversion in NSE Equities
### Full Dataset Evidence: 2007-2025

**Status:** Confirmed finding
**Supersedes:** RN001 (2007 preliminary)

---

## Summary

NSE equities exhibit strong, persistent, regime-independent cross-sectional
mean reversion across 18 years of daily data. Stocks with the worst recent
returns systematically outperform stocks with the best recent returns.

A monthly-rebalanced contrarian strategy generates +83% gross annual return.
After worst-case transaction costs (3% round trip), net return is +47%.
T-statistics exceed 5 on both the long and short legs.

---

## Data

- Source: Mendeley NSE dataset
- Universe: 85 NSE equities with price data
- Tradeable universe: 59 stocks (avg daily volume >= 10,000 shares)
- Period: 2007-01-02 to 2025-10-31
- Observations: 249,488 daily returns
- Exclusions: Returns > 100% in absolute value (14 rows, data quality)

---

## Market Context

NSE 20 total return 2007-2025: -45.7%
The market has been predominantly bearish over this period.
12 negative years, 7 positive years.
Extended bear period: 2015-2023.
Strong recovery: 2024 (+33%), 2025 (+51% YTD).

---

## Efficiency Tests

| Metric | Value |
|--------|-------|
| Mean lag-1 AC (full universe) | -0.078 |
| Mean lag-1 AC (tradeable) | -0.081 |
| Momentum stocks (AC > 0) | 7/83 |
| Mean reversion stocks (AC < 0) | 73/83 |
| Statistically predictable (LB p<0.05) | 72/83 |

---

## Quintile Analysis — 20d Momentum Factor

Monthly rebalancing, long Q1 (losers) only.

| Quintile | Ann Return | T-stat |
|----------|------------|--------|
| Q1 (losers) | +83.2% | +5.51 |
| Q2 | -2.2% | -0.17 |
| Q3 | +0.5% | +0.05 |
| Q4 | -18.7% | -1.55 |
| Q5 (winners) | -71.3% | -5.06 |

Long-short spread: -154.5% annualized.

---

## Transaction Cost Analysis

| Round Trip Cost | Net Annual Return |
|-----------------|-------------------|
| 0.5% | +77.2% |
| 1.0% | +71.2% |
| 2.0% | +59.2% |
| 3.0% | +47.2% |

Break-even round trip: 13.87% — impossible to reach in practice.

---

## Regime Analysis

| Regime | Years | Q1 Return | T-stat |
|--------|-------|-----------|--------|
| Bull | 2009,2010,2012,2013,2017,2024,2025 | +89.0% | +5.14 |
| Bear | 2008,2011,2015,2016,2018,2020 | +83.6% | +2.07 |
| Flat | 2007,2014,2019,2021,2022,2023 | +74.7% | +3.84 |

Finding: strategy works in all market regimes.
Not cyclical — structural.

---

## Sector Analysis

| Sector | Q1 Return | Q5 Return |
|--------|-----------|-----------|
| Agricultural | +66.1% | +18.2% |
| Banking | +65.9% | -77.5% |
| Insurance | +50.4% | 0.0% |
| Manufacturing | +34.1% | -41.8% |

Banking is the priority sector for live trading:
most liquid, strong effect on both legs.

---

## Economic Interpretation

Slow price discovery in an illiquid frontier market.
Large relative price moves reflect temporary order imbalances
rather than genuine information. Subsequent mean reversion
as the imbalance clears.

Effect strongest at 20d lookback — consistent with monthly
liquidity cycles in a market with limited active participants.

No short selling mechanism on NSE — long-only contrarian
is the implementable strategy.

---

## Next Steps

1. Efficiency evolution — is the effect weakening over time?
2. Value and size factors — independent sources of return?
3. Factor combination — does combining factors improve Sharpe?
4. Proper backtest — transaction costs, slippage, position limits
5. Position sizing — Kelly criterion for optimal bet sizing
6. Paper trading — 3 month live validation before real capital

---

*Nairobi Alpha Research — May 2026*
