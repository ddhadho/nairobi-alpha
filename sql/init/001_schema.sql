-- =============================================================================
-- NAIROBI ALPHA — Database Schema
-- =============================================================================

-- Securities master table
-- Every listed security, active or delisted
CREATE TABLE IF NOT EXISTS securities (
    security_id     SERIAL PRIMARY KEY,
    ticker          VARCHAR(20) UNIQUE NOT NULL,
    name            VARCHAR(200),
    sector          VARCHAR(100),
    industry        VARCHAR(100),
    listing_date    DATE,
    delisting_date  DATE,
    currency        VARCHAR(10) DEFAULT 'KES',
    security_type   VARCHAR(50) DEFAULT 'equity', -- equity, preference, etf, reit, index
    is_active       BOOLEAN DEFAULT TRUE,
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Daily price data
-- One row per security per trading day
-- Stores both nominal and adjusted prices as found in source data
CREATE TABLE IF NOT EXISTS prices (
    price_id        SERIAL PRIMARY KEY,
    security_id     INTEGER NOT NULL REFERENCES securities(security_id),
    date            DATE NOT NULL,
    day_low         NUMERIC(15,4),
    day_high        NUMERIC(15,4),
    close           NUMERIC(15,4),      -- nominal closing price
    previous_close  NUMERIC(15,4),      -- previous day nominal close
    change_abs      NUMERIC(15,4),      -- absolute change
    change_pct      NUMERIC(10,6),      -- percentage change as decimal (0.05 = 5%)
    volume          BIGINT,
    adjusted_close  NUMERIC(15,4),      -- split-adjusted close from source
    week52_low      NUMERIC(15,4),      -- 52 week low
    week52_high     NUMERIC(15,4),      -- 52 week high
    split_factor    NUMERIC(15,6),      -- computed: close / adjusted_close
    source          VARCHAR(50) DEFAULT 'mendeley_2007',
    UNIQUE(security_id, date)
);

-- Computed returns table
-- Populated after prices are loaded
-- Storing returns separately avoids recomputing repeatedly
CREATE TABLE IF NOT EXISTS returns (
    return_id           SERIAL PRIMARY KEY,
    security_id         INTEGER NOT NULL REFERENCES securities(security_id),
    date                DATE NOT NULL,
    daily_return        NUMERIC(15,8),      -- log return: ln(close_t / close_t-1)
    daily_return_simple NUMERIC(15,8),      -- simple return: (close_t - close_t-1) / close_t-1
    adj_daily_return    NUMERIC(15,8),      -- log return using adjusted close
    UNIQUE(security_id, date)
);

-- Corporate actions
-- Splits, dividends, rights issues, bonus shares
CREATE TABLE IF NOT EXISTS corporate_actions (
    action_id       SERIAL PRIMARY KEY,
    security_id     INTEGER NOT NULL REFERENCES securities(security_id),
    action_date     DATE NOT NULL,
    action_type     VARCHAR(50) NOT NULL,   -- split, dividend_cash, rights, bonus
    factor          NUMERIC(15,6),          -- split ratio, dividend amount, etc
    ex_date         DATE,
    record_date     DATE,
    payment_date    DATE,
    details         JSONB,
    source          VARCHAR(100),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Fundamental data
-- Financial statement data, annual and interim
CREATE TABLE IF NOT EXISTS fundamentals (
    fundamental_id  SERIAL PRIMARY KEY,
    security_id     INTEGER NOT NULL REFERENCES securities(security_id),
    period_end      DATE NOT NULL,
    period_type     VARCHAR(20) NOT NULL,   -- annual, interim_h1, interim_q1 etc
    revenue         NUMERIC(20,2),
    net_income      NUMERIC(20,2),
    total_assets    NUMERIC(20,2),
    total_equity    NUMERIC(20,2),
    total_debt      NUMERIC(20,2),
    cash            NUMERIC(20,2),
    earnings_ps     NUMERIC(15,4),          -- earnings per share
    book_value_ps   NUMERIC(15,4),          -- book value per share
    dividend_ps     NUMERIC(15,4),          -- dividend per share
    shares_outstanding BIGINT,
    roe             NUMERIC(10,6),          -- return on equity
    roa             NUMERIC(10,6),          -- return on assets
    source          VARCHAR(100),
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(security_id, period_end, period_type)
);

-- Market indices
-- NSE 20, NSE 25, NASI, NSE All Share etc
CREATE TABLE IF NOT EXISTS indices (
    index_id        SERIAL PRIMARY KEY,
    date            DATE NOT NULL,
    nse_20          NUMERIC(15,4),
    nse_25          NUMERIC(15,4),
    nse_all_share   NUMERIC(15,4),
    nse_10          NUMERIC(15,4),
    bonds_index     NUMERIC(15,4),
    volume          BIGINT,
    UNIQUE(date)
);

-- Computed factors
-- Stores factor values for each security each date
-- Flexible design: any factor name, no schema changes needed for new factors
CREATE TABLE IF NOT EXISTS factors (
    factor_id       SERIAL PRIMARY KEY,
    security_id     INTEGER NOT NULL REFERENCES securities(security_id),
    date            DATE NOT NULL,
    factor_name     VARCHAR(100) NOT NULL,
    factor_value    NUMERIC(15,8),
    factor_rank     INTEGER,                -- cross-sectional rank on this date
    factor_zscore   NUMERIC(10,6),          -- cross-sectional z-score on this date
    created_at      TIMESTAMP DEFAULT NOW(),
    UNIQUE(security_id, date, factor_name)
);

-- Research runs
-- Every backtest, every analysis — logged here
-- Full reproducibility: parameters in, results out
CREATE TABLE IF NOT EXISTS research_runs (
    run_id          SERIAL PRIMARY KEY,
    run_date        TIMESTAMP DEFAULT NOW(),
    run_type        VARCHAR(100),           -- backtest, factor_analysis, efficiency_test etc
    strategy_name   VARCHAR(200),
    description     TEXT,
    parameters      JSONB,                  -- all input parameters
    results         JSONB,                  -- all output metrics
    notes           TEXT,
    is_significant  BOOLEAN                 -- did this finding pass statistical tests?
);

-- Data quality log
-- Track every data issue found and how it was handled
CREATE TABLE IF NOT EXISTS data_quality_log (
    log_id          SERIAL PRIMARY KEY,
    log_date        TIMESTAMP DEFAULT NOW(),
    security_id     INTEGER REFERENCES securities(security_id),
    date            DATE,
    issue_type      VARCHAR(100),           -- missing_value, outlier, zero_price etc
    description     TEXT,
    resolution      VARCHAR(100),           -- imputed, dropped, flagged etc
    details         JSONB
);

-- =============================================================================
-- INDEXES
-- Performance indexes for common research queries
-- =============================================================================

-- Prices: most queries filter by security and date range
CREATE INDEX IF NOT EXISTS idx_prices_security_date
    ON prices(security_id, date DESC);

CREATE INDEX IF NOT EXISTS idx_prices_date
    ON prices(date DESC);

-- Returns: same pattern
CREATE INDEX IF NOT EXISTS idx_returns_security_date
    ON returns(security_id, date DESC);

CREATE INDEX IF NOT EXISTS idx_returns_date
    ON returns(date DESC);

-- Factors: queries usually filter by factor name and date
CREATE INDEX IF NOT EXISTS idx_factors_name_date
    ON factors(factor_name, date DESC);

CREATE INDEX IF NOT EXISTS idx_factors_security_date
    ON factors(security_id, date DESC);

-- Securities: frequent lookup by ticker
CREATE INDEX IF NOT EXISTS idx_securities_ticker
    ON securities(ticker);

-- =============================================================================
-- VIEWS
-- Common query patterns as views for convenience in research notebooks
-- =============================================================================

-- Price data joined with security info
CREATE OR REPLACE VIEW v_prices AS
    SELECT
        p.*,
        s.ticker,
        s.name,
        s.sector,
        s.security_type,
        s.is_active
    FROM prices p
    JOIN securities s ON p.security_id = s.security_id;

-- Returns joined with security info
CREATE OR REPLACE VIEW v_returns AS
    SELECT
        r.*,
        s.ticker,
        s.name,
        s.sector
    FROM returns r
    JOIN securities s ON r.security_id = s.security_id;

-- Active equity securities only
CREATE OR REPLACE VIEW v_equity_universe AS
    SELECT *
    FROM securities
    WHERE security_type = 'equity'
    AND is_active = TRUE
    AND delisting_date IS NULL;

-- =============================================================================
-- METADATA
-- =============================================================================

CREATE TABLE IF NOT EXISTS metadata (
    key             VARCHAR(100) PRIMARY KEY,
    value           TEXT,
    updated_at      TIMESTAMP DEFAULT NOW()
);

INSERT INTO metadata (key, value) VALUES
    ('schema_version', '1.0'),
    ('project_name', 'Nairobi Alpha'),
    ('created', NOW()::TEXT)
ON CONFLICT (key) DO NOTHING;