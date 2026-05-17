# Nairobi Alpha

Quantitative research engine for the Nairobi Securities Exchange.

Finding the subtle order in NSE's apparent chaos.

---

## Current Status

**Phase 3 — Active Research**

Core finding confirmed across 18 years of data. Mean reversion is
persistent, statistically significant, and regime-independent.

---

## Key Findings

### RN002 — Cross-Sectional Mean Reversion (2007-2025)
- 54/59 tradeable stocks show negative lag-1 autocorrelation
- Mean lag-1 AC: -0.081 across tradeable universe
- 72/83 stocks statistically predictable (Ljung-Box p < 0.05)
- 20d contrarian strategy: +83% gross annual return
- Net return at 3% round trip (worst case): +47% annually
- T-statistics: Q1 +5.51, Q5 -5.06
- Holds across all regimes: bull +89%, bear +84%, flat +75%
- Strongest tradeable effect: Banking sector (Q1 +66%, Q5 -78%)
- Monthly rebalancing viable at any realistic NSE transaction cost

### RN001 — Preliminary 2007 Finding (superseded by RN002)
Single year result. Confirmed and extended by RN002.

---

## Dataset

Source: Mendeley NSE dataset

- Annual all-stocks files: 2007-2025 (19 files)
- Individual stock files: 98 files across 14 sector directories
- Index data: NSE 20, NSE 25, NASI, Bonds Index

Database (PostgreSQL):
- 289,498 price rows
- 249,488 return rows
- 97 securities
- 19 years: 2007-01-02 to 2025-10-31

---

## Research Agenda

- [x] Market efficiency tests — autocorrelation, Ljung-Box
- [x] Mean reversion factor — confirmed, regime-tested, sector-tested
- [x] Efficiency evolution — stable, p=0.76, edge is durable
- [x] Value factors — price-to-book, dividend yield
- [x] Size factor — small cap premium
- [x] Liquidity factor — illiquidity premium
- [x] Factor independence — N/A (only one factor survived)
- [ ] Risk model — covariance structure
- [ ] Backtester — realistic simulation with NSE costs
- [ ] Position sizing — Kelly criterion
- [ ] Paper trading — 3 month live validation

---

## Setup

```bash
# Environment
pip install -r requirements.txt
cp .env.example .env
# Set DB_PASSWORD and DB_PORT=5433 in .env

# Database
docker-compose up -d

# Load all data
python3 -c "
import sys; sys.path.insert(0, '.')
from src.data.cleaning.nse_cleaner import load_and_clean, compute_returns
from src.data.storage.database import get_engine, upsert_securities, insert_prices, insert_returns, insert_indices
from pathlib import Path
engine = get_engine()
for f in sorted(Path('data/raw').glob('NSE_data_all_stocks_*.csv')):
    prices, indices, quality = load_and_clean(f)
    equities = prices[prices['security_type']=='equity']
    returns = compute_returns(equities)
    ids = upsert_securities(prices, engine)
    insert_prices(prices, ids, engine)
    insert_returns(returns, ids, engine)
    insert_indices(indices, engine)
    print(f'{f.name}: done')
"

# Research
jupyter lab notebooks/

---

*Nairobi Alpha — Finding the subtle order in NSE's chaos.*
