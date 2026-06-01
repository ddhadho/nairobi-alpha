# Nairobi Alpha — Research Note 006
## Strategy Backtest: NSE Contrarian Strategy 2007-2025

**Status:** Confirmed — strategy not viable at retail costs
**Date:** May 2026

---

## Summary

The NSE mean reversion factor (RN002) is statistically real.
A properly constructed backtest shows it is not currently
viable as a retail trading strategy due to transaction costs
and variance drag. Institutional implementation may be viable.

---

## Backtest Methodology

**Strategy:** Monthly contrarian — buy 15 biggest 20-day losers
**Universe:** NSE equities with avg daily volume >= 10,000 shares
**Period:** 2008-01-02 to 2025-10-16 (17.8 years)
**Starting capital:** KES 100,000
**Rebalancing:** Rolling, every N trading days
**Costs:** Applied on turnover at each rebalance

---

## Holding Period Analysis — Gross Returns

| Hold (days) | Mean Period Return | Arithmetic Ann | Geometric CAGR |
|-------------|-------------------|----------------|----------------|
| 1 | +0.161% | +49.8% | +21.2% |
| 3 | +0.246% | +22.9% | +8.0% |
| 5 | +0.346% | +19.0% | +4.8% |
| 10 | +0.370% | +9.8% | -1.1% |
| 15 | +0.122% | +2.1% | -4.3% |
| 21 | -0.836% | -9.6% | -14.3% |

**Key finding:** Signal decays within 5-7 days.
Holding longer than 5 days destroys returns.
Even at 1-day holding, variance drag reduces
arithmetic return of 49.8% to geometric CAGR of 21.2%.

---

## Net Returns After Transaction Costs

| Hold (days) | Gross CAGR | Net @3.5% | Net @1.5% | Net @0.5% |
|-------------|------------|-----------|-----------|-----------|
| 1 | +21.2% | -77.7% | -41.3% | -4.8% |
| 3 | +8.0% | -52.7% | -24.1% | -3.9% |
| 5 | +4.8% | -42.2% | -18.7% | -3.7% |
| 10 | -1.1% | -31.7% | -15.6% | -6.2% |
| 15 | -4.3% | -28.5% | -15.5% | -8.2% |
| 21 | -14.3% | -32.0% | -22.3% | -17.1% |

**No holding period is viable at retail (3.5%) or
negotiated (1.5%) transaction cost levels.**

---

## Why The Strategy Fails

### 1. Variance Drag
The strategy holds extreme recent losers — the most volatile
stocks on NSE. Portfolio annual volatility: ~50-70%.

Geometric return ≈ Arithmetic return − (Variance² / 2)
49.8% − (60%² / 2) = 49.8% − 18% = ~32% theoretical
Actual geometric: 21.2% — further reduced by compounding path

### 2. Transaction Costs
NSE retail round trip: ~3.5%
At 1-day holding with 60% daily turnover:
Annual cost = 252 × 0.60 × 3.5% = 529% of capital
This exceeds any realistic gross return.

### 3. Signal Horizon Mismatch
The factor predicts next-day returns correctly (t-stat 5.51).
After day 1 the signal has decayed.
Holding beyond day 1 means holding random volatile stocks.

---

## Actual Backtest Results (5-day holding, 2% cost)

| Metric | Value |
|--------|-------|
| Starting capital | KES 100,000 |
| Final capital | KES 558 |
| Total return | -99.4% |
| CAGR | -25.3% |
| Max drawdown | -99.7% |
| Sharpe ratio | 0.812 |
| Win rate | 52.9% |

The positive Sharpe and win rate confirm the signal is real.
The negative CAGR reflects variance drag and costs overwhelming
the signal.

---

## What Would Make It Viable

### Option A — Institutional Costs
Need < 0.3% round trip.
Requires significant AUM and broker negotiation.
At 0.1% round trip (institutional): 1-day holding
gross CAGR of 21.2% would likely survive.
Not accessible at individual investor scale currently.

### Option B — Reduce Portfolio Volatility
Hold 30-40 stocks instead of 15.
Filter out most volatile stocks from universe.
Accept lower gross return for significantly lower variance drag.
May turn strategy viable at negotiated cost levels.
Buildable immediately with existing infrastructure.

### Option C — Crypto Application
Same mean reversion research applied to crypto markets.
Binance transaction costs: ~0.1% round trip (35x cheaper).
Same statistical effect would generate viable net returns.
Accessible from Kenya immediately.

### Option D — Academic Contribution
The finding has genuine value as research even if
not retail-tradeable. Publish on SSRN. Build institutional
credibility. Institutional investors with cost advantages
can exploit the finding directly.

---

## Statistical Validity Confirmed

The backtest failure does not invalidate the research finding.

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Lag-1 AC mean | -0.081 | Strong mean reversion |
| Ljung-Box significant | 72/83 stocks | Genuine predictability |
| Q1 t-stat | +5.51 | Highly significant |
| Regime stability | All regimes | Structural not cyclical |
| Time trend p-value | 0.76 | Not disappearing |

The anomaly is real. The implementation challenge is real.
Both are true simultaneously.

---

## Next Steps

1. Test Option B — volatility-filtered universe backtest
2. Test Option C — apply research to crypto markets
3. Continue building institutional credibility via SSRN
4. Monitor NSE transaction cost environment for changes

---

## Lessons

This is how quantitative research works.
Most statistically significant factors do not survive
realistic implementation. The gap between statistical
and economic significance is the central challenge.

Finding this gap through rigorous backtesting is
a genuine research contribution — not a failure.
It took 18 years of data and a proper backtester
to discover it. That is the work.

---

*Nairobi Alpha Research — May 2026*
