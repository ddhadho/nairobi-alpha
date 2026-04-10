# Nairobi Alpha — Research Note 001
## Cross-Sectional Mean Reversion in NSE Equities
### Evidence from 2007 Daily Data

**Date:** First research session  
**Status:** Preliminary — requires replication across full dataset  
**Author:** Nairobi Alpha Research

---

## Summary

NSE 2007 daily data shows statistically significant cross-sectional mean 
reversion. Stocks with the worst recent returns (Q1) outperform stocks with 
the best recent returns (Q5) over the subsequent trading day. This pattern 
holds across 5d, 10d, and 20d lookback windows with t-statistics ranging 
from -3.8 to -4.6.

**Key finding:** A contrarian strategy (long recent losers, short recent 
winners) would have generated approximately 100-112% annualized long-short 
spread in 2007. This is a large effect in a single year and must be treated 
with appropriate caution.

---

## Data

- Source: NSE Mendeley dataset, 2007 calendar year
- Universe: 50 NSE-listed equities
- Tradeable universe (avg vol > 10,000 shares/day): 40 stocks
- Trading days: 248
- Return metric: log returns of split-adjusted closing prices

---

## Methodology

**Factor construction:**
- Momentum_Nd = cumulative log return over past N trading days, skip 1 day
- Computed for N = 5, 10, 20 days

**Cross-sectional test:**
- On each trading date, sort stocks into quintiles by momentum factor
- Q1 = lowest momentum (recent losers), Q5 = highest (recent winners)
- Compute equal-weighted forward 1-day return for each quintile
- Long-short spread = Q5 return - Q1 return

**Information Coefficient:**
- Spearman rank correlation between momentum and next-day return
- Computed daily across all stocks with valid data
- Mean IC and t-statistic reported

---

## Results

| Window | Mean IC | T-stat | Q1 Ann | Q5 Ann | L/S Spread |
|--------|---------|--------|--------|--------|------------|
| 5d     | -0.048  | -3.83  | +62.1% | -50.4% | -112.6%    |
| 10d    | -0.060  | -4.58  | —      | —      | —          |
| 20d    | -0.047  | -3.86  | +61.7% | -48.3% | -110.0%    |

All mean ICs are negative and statistically significant (p < 0.01).  
The pattern is consistent across lookback windows.

---

## Reconciliation With Autocorrelation Finding

The positive mean lag-1 autocorrelation (+0.065) found in the same dataset 
appears to contradict this mean reversion finding. The reconciliation:

**Autocorrelation** measures time-series persistence for individual stocks.
A stock that rose yesterday tends to rise again today — in absolute terms.

**Cross-sectional mean reversion** measures relative performance.
A stock that rose more than its peers recently tends to underperform its 
peers going forward.

These can coexist when there is a strong market-wide factor. In 2007, NSE 
experienced significant price appreciation in specific sectors (banking, 
insurance) followed by corrections. Stocks that had the highest relative 
gains were most exposed to subsequent mean reversion while the overall 
market maintained positive time-series momentum.

This pattern — time-series momentum + cross-sectional mean reversion — 
has been documented in other frontier and emerging markets.

---

## Economic Interpretation

Several mechanisms could explain cross-sectional mean reversion in NSE:

**1. Liquidity-driven overshooting**
In a thin market, large relative price moves require very little capital.
A stock rising 20% in a week may reflect a single large order rather than 
genuine information. Subsequent mean reversion occurs as the temporary 
price pressure dissipates.

**2. Correlated retail sentiment**
Kenyan retail investors in 2007 may have chased recent winners, 
pushing prices above fundamental value, followed by correction.

**3. Attention effects**
Stocks with large recent gains attract attention and buying, overshooting 
fair value. Losers attract selling, undershooting. Both revert.

**4. Low analyst coverage**
With minimal analyst coverage, there is no mechanism to quickly identify 
and arbitrage away cross-sectional mispricings. Mean reversion may simply 
be slow correction of sentiment-driven mispricing.

---

## Limitations and Cautions

1. **Single year** — 2007 was unusual globally (pre-GFC bull market)
   and locally (NSE bull market). Results may not generalize.

2. **Small universe** — 40 tradeable stocks means only 8 per quintile.
   Quintile construction is noisy with this few securities.

3. **Transaction costs** — A strategy trading daily would face significant
   NSE bid-ask spreads (estimated 0.5-1.5% round trip for liquid stocks).
   After realistic costs, the net spread would be substantially smaller.

4. **Short selling** — NSE did not have liquid short selling in 2007.
   The "short" leg of this strategy was not practically implementable.
   Long-only contrarian (buying losers only) is the implementable version.

5. **One year of data** — t-statistics of 3-4 are meaningful but a single 
   year of daily data (248 observations) has limited degrees of freedom.
   Replication across 2007-2024 is required before any conclusions hold.

---

## Next Steps

1. Acquire full NSE dataset 2007-2024 from Mendeley
2. Replicate mean reversion test across all years
3. Test stability across different market regimes (bull/bear/crisis)
4. Compute net-of-cost returns using realistic NSE transaction costs
5. Test long-only contrarian strategy (buying Q1 stocks)
6. Compare NSE mean reversion to documented effects in other African markets
7. Investigate whether effect is stronger in specific sectors or liquidity cohorts

---

## Significance

If this mean reversion effect persists across the full dataset, it would 
represent a genuine, exploitable inefficiency in NSE with the following 
characteristics:

- **Source of edge**: Slow information incorporation in illiquid frontier market
- **Implementation**: Long-only contrarian for practical trading
- **Risk**: Concentrated in specific stocks, illiquidity risk on exit
- **Competition**: Near zero — no known systematic research on NSE factors

This is the kind of original finding — specific to this market, invisible 
to global researchers, grounded in local market structure — that Nairobi 
Alpha exists to discover.

---

*Research Note 001 — Nairobi Alpha*  
*Preliminary findings. Not for distribution. Requires full dataset replication.*
