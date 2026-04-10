# Nairobi Alpha

Quantitative research engine for the Nairobi Securities Exchange.

---

## What This Is

A systematic quantitative research infrastructure for NSE equities.
Built from scratch on 18 years of NSE data (2007-2025).

**Research agenda:**
- Market efficiency — is NSE predictable?
- Factor premia — momentum, mean reversion, value, size, liquidity
- Regime analysis — how do strategies perform across bull/bear markets?
- Risk model — covariance structure, systematic factors
- Sector dynamics — how do NSE sectors relate to macro variables?

**Current finding (2007 data):**
NSE shows statistically significant cross-sectional mean reversion.
Recent losers outperform recent winners by ~110% annualized long-short
spread. Effect consistent across 5d, 10d, 20d lookback windows.
T-statistics: 3.8–4.6. Needs replication across full dataset.

---

## Dataset

Source: Mendeley NSE dataset
- Annual all-stocks files: 2007–2025 (19 files, ~190,000 rows)
- Individual stock historical files: 98 files across 14 sector directories
- Sector aggregate files: 2013, 2020–2025
- Index data: NSE 20, NASI, FTSE Kenya 15, FTSE Kenya 25

---

## Setup

### 1. Environment

```bash
# Clone and navigate
cd nairobi_alpha

# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
# Edit .env with your database password
```

### 2. Database

```bash
# Start PostgreSQL via Docker
docker-compose up -d

# Verify it is running
docker ps

# Schema is auto-applied on first start
# (sql/init/001_schema.sql is mounted as init script)
```

### 3. Load All Data

```bash
# Point to your Mendeley dataset directory
python setup_and_run.py --data-dir /path/to/mendeley/data

# Skip database if you want research only
python setup_and_run.py --data-dir /path/to/mendeley/data --skip-db
```

### 4. Research Notebooks

```bash
# Start Jupyter
jupyter lab notebooks/
```

---

## Project Structure

```
nairobi-alpha/
│
├── docker/
│   ├── jupyter/
│   │   └── Dockerfile
│   └── postgres/
│       └── Dockerfile
│
├── sql/
│   ├── init/
│   │   └── 001_schema.sql
│   └── queries/
│       └── (saved research queries)
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── acquisition/
│   │   │   ├── __init__.py
│   │   │   ├── nse_scraper.py
│   │   │   └── corporate_actions.py
│   │   ├── cleaning/
│   │   │   ├── __init__.py
│   │   │   ├── price_cleaner.py
│   │   │   └── adjustment.py
│   │   └── storage/
│   │       ├── __init__.py
│   │       └── database.py
│   │
│   ├── research/
│   │   ├── __init__.py
│   │   ├── returns/
│   │   │   ├── __init__.py
│   │   │   └── calculator.py
│   │   ├── factors/
│   │   │   ├── __init__.py
│   │   │   ├── momentum.py
│   │   │   ├── value.py
│   │   │   ├── size.py
│   │   │   ├── quality.py
│   │   │   └── liquidity.py
│   │   ├── statistics/
│   │   │   ├── __init__.py
│   │   │   ├── efficiency_tests.py
│   │   │   └── factor_tests.py
│   │   └── risk/
│   │       ├── __init__.py
│   │       └── covariance.py
│   │
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── backtester.py
│   │   ├── portfolio.py
│   │   └── performance.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logging.py
│
├── notebooks/
│   ├── 01_data_exploration/
│   ├── 02_efficiency_research/
│   ├── 03_factor_research/
│   ├── 04_strategy_development/
│   └── 05_risk_research/
│
├── research/
│   └── papers/
│       └── (your written research outputs)
│
├── tests/
│   └── (unit tests for core components)
│
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
└── setup_and_run.py         # Master setup script
```

---

## Running The Full Research Agenda

Once all data is loaded:

```python
from src.data.acquisition.ingest import ingest_all_annual_files
from src.research.engine import run_full_research

# Load all years
prices, indices, returns = ingest_all_annual_files(Path('data/raw'))

# Run everything
results = run_full_research(prices, returns, indices)
```

---

## Key Findings So Far

### RN001 — Cross-Sectional Mean Reversion (2007)
NSE 2007 shows strong mean reversion across 5d/10d/20d windows.
Q1 (recent losers): +62% ann. Q5 (recent winners): -50% ann.
L/S spread: -112% ann. T-stat: -3.8 to -4.6.
Status: Preliminary. Requires full dataset replication.

---

