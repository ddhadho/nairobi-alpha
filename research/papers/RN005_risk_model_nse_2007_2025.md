# Nairobi Alpha — Research Note 005
## NSE Risk Model: Correlation Structure and Portfolio Construction
### 2007-2025

**Status:** Confirmed
**Date:** May 2026

---

## Summary

NSE equities are weakly correlated with high idiosyncratic risk.
The market factor explains only 27% of return variance.
A 10-15 stock equal-weighted portfolio captures adequate diversification.

---

## Correlation Structure

| Metric | Value |
|--------|-------|
| Mean pairwise correlation | 0.168 |
| Median pairwise correlation | 0.111 |
| % positive pairs | 87.6% |
| % pairs > 0.3 | 23.4% |
| Max correlation | 0.742 (MSC-KPLC, likely spurious) |
| Min correlation | -0.168 (UCHM-KQ) |

NSE stocks are weakly correlated compared to developed markets
(US average: 0.3-0.5). Significant diversification opportunity exists.

Notable: MSC (Mumias Sugar) shows spuriously high correlations
due to near-zero variance in a suspended/distressed stock. 
Exclude from strategy universe.

---

## PCA Factor Structure

| Components | Variance Explained |
|------------|-------------------|
| PC1 (market) | 27.3% |
| 6 components | 50.1% |
| 16 components | 70.0% |
| 34 components | 90.0% |

The market factor is weak at 27% — much lower than developed markets.
NSE returns are driven by stock-specific factors more than market-wide moves.
High idiosyncratic risk means stock selection dominates portfolio returns.

---

## Portfolio Diversification

| Portfolio Size | Ann Volatility | Reduction vs 1 Stock |
|---------------|----------------|---------------------|
| 1 stock | 66.9% | — |
| 5 stocks | 57.6% | 14% |
| 10 stocks | 50.9% | 24% |
| 15 stocks | 49.4% | 26% |
| 20 stocks | 48.0% | 28% |

Diversification benefit plateaus sharply after 15 stocks.
Going from 15 to 20 stocks reduces volatility by only 1.4%.
High idiosyncratic risk means even large portfolios remain volatile.

---

## Portfolio Construction Recommendations

**Target size:** 10-15 stocks
**Weighting:** Equal weight — no complex optimization needed
**Universe:** Stocks with average daily volume >= 10,000 shares
**Sector focus:** Banking — most liquid, strongest mean reversion
**Rebalancing:** Monthly — consistent with 20d factor signal
**Exclude:** Suspended stocks, stocks with near-zero trading volume

---

## Implications for Nairobi Alpha Strategy

The weak market factor and high idiosyncratic risk confirm that
the cross-sectional mean reversion strategy is well-suited for NSE.

The strategy profits from stock-specific variance — exactly what
NSE has in abundance. A long-only contrarian portfolio of 10-15
stocks from the Q1 (biggest recent losers) quintile, rebalanced
monthly, is the correct implementation.

Expected portfolio characteristics:
- Gross return: ~83% ann (from RN002 Q1 quintile)
- Portfolio volatility: ~50% ann (10-15 stocks)
- Gross Sharpe ratio: ~1.66
- After 3% round trip costs: ~47% net, Sharpe ~0.94

---

*Nairobi Alpha Research — May 2026*
