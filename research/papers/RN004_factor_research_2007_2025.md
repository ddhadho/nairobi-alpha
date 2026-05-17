# Nairobi Alpha — Research Note 004
## Factor Research Results: NSE 2007-2025

**Status:** Confirmed
**Date:** May 2026

---

## Summary

Five factors tested on NSE daily data 2007-2025.
One confirmed. Four rejected.

---

## Factors Tested

### 1. Short-horizon Mean Reversion (20d) — CONFIRMED

The primary Nairobi Alpha factor. Documented in RN002.

| Metric | Value |
|--------|-------|
| Q1 gross return | +83.2% ann |
| Q5 gross return | -71.3% ann |
| L/S spread | -154.5% ann |
| Q1 t-stat | +5.51 |
| Q5 t-stat | -5.06 |

Holds across all regimes. Durable across 18 years (RN003).

---

### 2. Long-horizon Value Proxies (6m, 12m) — REJECTED

Hypothesis: long-term losers outperform (value effect).

| Factor | Q1 Return | T-stat |
|--------|-----------|--------|
| 6m momentum | -7.9% | -0.53 |
| 12m momentum | -12.5% | -0.83 |

Not significant. Wrong direction.

Long-horizon losers continue falling on NSE.
They reflect genuine fundamental deterioration,
not temporary mispricing.

Note: 52-week range data in source files is unreliable.
True value factors (P/B, dividend yield) require
fundamental data — backlogged for individual stock files.

---

### 3. Size Factor (volume proxy) — REJECTED

Hypothesis: small cap stocks outperform large cap stocks.

| Quintile | Return | T-stat |
|----------|--------|--------|
| Q1 (small) | +4.4% | +0.38 |
| Q5 (large) | +5.7% | +0.35 |
| Size premium | -1.4% | — |

Not significant. No size premium on NSE.

NSE small caps are illiquid distressed companies,
not overlooked growth stocks. Transaction costs
eliminate any theoretical premium.

---

### 4. Illiquidity Factor (Amihud measure) — REJECTED

Hypothesis: illiquid stocks earn higher returns
as compensation for liquidity risk.

| Quintile | Return | T-stat |
|----------|--------|--------|
| Q1 (liquid) | +1.9% | +0.12 |
| Q5 (illiquid) | +2.3% | +0.16 |
| Illiquidity premium | +0.4% | — |

Not significant. No illiquidity premium on NSE.

Same reason as size — illiquid NSE stocks are
genuinely bad companies, not just overlooked.
Exit risk makes illiquid positions dangerous.

---

## Factor Scorecard

| Factor | Q1 Return | T-stat | Decision |
|--------|-----------|--------|----------|
| 20d mean reversion | +83.2% | +5.51 | ✅ CONFIRMED |
| 6m value proxy | -7.9% | -0.53 | ❌ REJECTED |
| 12m value proxy | -12.5% | -0.83 | ❌ REJECTED |
| Size (volume) | +4.4% | +0.38 | ❌ REJECTED |
| Illiquidity (Amihud) | +2.3% | +0.16 | ❌ REJECTED |

---

## Implications

Only one factor survives rigorous testing.
This is normal in quantitative research —
most factors do not hold up under scrutiny.

The 20d mean reversion factor is the foundation
of the Nairobi Alpha trading strategy.

Future research with fundamental data may uncover
genuine value factors. Backlogged.

---

## Research Backlog

- True value factors: P/B, dividend yield, earnings yield
  Requires ingesting individual stock fundamental data
- Quality factor: ROE, earnings stability
  Same data requirement
- Cross-asset signals: EAC commodity prices, macro data

---

*Nairobi Alpha Research — May 2026*
