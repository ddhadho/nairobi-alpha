"""
nairobi_alpha.research.factors.momentum
=========================================
Momentum factor construction for NSE.

Momentum is the tendency for recent winners to continue outperforming
and recent losers to continue underperforming. It is one of the most
robust factors in global equity markets.

The classic Jegadeesh-Titman (1993) momentum uses 12-month past returns
skipping the most recent month (12-1 momentum) to avoid short-term reversal.

For NSE we test multiple lookback windows given the market's unique
microstructure and liquidity characteristics.

Research Question: Does momentum exist in NSE?
Hypothesis: Yes — the positive lag-1 autocorrelation observed in 2007
suggests slow price discovery consistent with momentum continuation.
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)




def compute_momentum(
    prices_df: pd.DataFrame,
    lookback_days: int = 20,
    skip_days: int = 1,
    min_observations: int = 15,
) -> pd.DataFrame:
    """
    Compute cross-sectional momentum factor for each stock on each date.

    Momentum = cumulative log return over [t - lookback - skip, t - skip]

    The skip_days parameter implements the short-term reversal skip.
    For daily data: skip=1 avoids bid-ask bounce.
    For monthly strategies: skip=21 (one month) is conventional.

    Parameters:
        prices_df       — cleaned prices with ticker, date, adjusted_close
        lookback_days   — momentum window in trading days
        skip_days       — days to skip before window starts (reversal avoidance)
        min_observations — minimum valid price observations required

    Returns:
        DataFrame with ticker, date, momentum_{N}d columns
    """
    results = []

    for ticker, group in prices_df.groupby('ticker'):
        g = group.sort_values('date').copy()
        adj = pd.to_numeric(g['adjusted_close'], errors='coerce')

        if adj.notna().sum() < min_observations + lookback_days + skip_days:
            continue

        # Log prices for cumulative return computation
        log_prices = np.log(adj)

        # Momentum: log return from (t - lookback - skip) to (t - skip)
        # This is: log_price[t-skip] - log_price[t-lookback-skip]
        momentum = log_prices.shift(skip_days) - log_prices.shift(lookback_days + skip_days)

        results.append(pd.DataFrame({
            'ticker': ticker,
            'date': g['date'].values,
            'adjusted_close': adj.values,
            f'momentum_{lookback_days}d': momentum.values,
        }))

    if not results:
        return pd.DataFrame()

    df = pd.concat(results, ignore_index=True)
    logger.info(
        f"Computed {lookback_days}d momentum for "
        f"{df['ticker'].nunique()} securities"
    )
    return df


def compute_momentum_multi(
    prices_df: pd.DataFrame,
    windows: list = [5, 10, 20, 60],
    skip_days: int = 1,
) -> pd.DataFrame:
    """
    Compute momentum for multiple lookback windows simultaneously.
    Useful for finding which window works best in NSE.

    Returns DataFrame with one row per (ticker, date) and
    one momentum column per window.
    """
    all_results = []

    for ticker, group in prices_df.groupby('ticker'):
        g = group.sort_values('date').copy()
        adj = pd.to_numeric(g['adjusted_close'], errors='coerce')
        log_prices = np.log(adj)

        row = {'ticker': ticker, 'date': g['date'].values}

        for w in windows:
            mom = log_prices.shift(skip_days) - log_prices.shift(w + skip_days)
            row[f'mom_{w}d'] = mom.values

        all_results.append(pd.DataFrame(row))

    if not all_results:
        return pd.DataFrame()

    return pd.concat(all_results, ignore_index=True)


def cross_sectional_rank(
    factor_df: pd.DataFrame,
    factor_col: str,
    date_col: str = 'date',
    ticker_col: str = 'ticker',
) -> pd.DataFrame:
    """
    Add cross-sectional rank and z-score for a factor.

    On each date, rank all securities by factor value.
    Rank 1 = lowest factor value. Rank N = highest.

    Also compute z-score: (factor - mean) / std on each date.
    Z-scores are better than raw values for combining factors.

    Parameters:
        factor_df  — DataFrame with ticker, date, factor column
        factor_col — name of the factor column to rank

    Returns:
        Input DataFrame with additional rank and zscore columns added
    """
    df = factor_df.copy()

    df[f'{factor_col}_rank'] = (
        df.groupby(date_col)[factor_col]
        .rank(method='average', na_option='keep')
    )

    # Percentile rank (0 to 1) — easier to interpret
    df[f'{factor_col}_pctrank'] = (
        df.groupby(date_col)[factor_col]
        .rank(method='average', pct=True, na_option='keep')
    )

    # Cross-sectional z-score
    group_stats = df.groupby(date_col)[factor_col].transform
    df[f'{factor_col}_zscore'] = (
        (df[factor_col] - group_stats('mean')) / group_stats('std')
    )

    return df


def momentum_quintile_returns(
    momentum_df: pd.DataFrame,
    returns_df: pd.DataFrame,
    factor_col: str,
    holding_period: int = 1,
    min_stocks_per_quintile: int = 3,
) -> pd.DataFrame:
    """
    Core factor research function.

    On each date, sort stocks into quintiles by momentum factor.
    Compute returns for each quintile over the next holding_period days.

    This is the standard Fama-French factor portfolio methodology.

    The key question: does Q5 (high momentum) outperform Q1 (low momentum)?
    If yes — momentum premium exists in NSE.
    If no — momentum does not generate alpha here.

    Parameters:
        momentum_df    — factor values with ticker, date, factor_col
        returns_df     — returns with ticker, date, log_return
        factor_col     — which momentum column to use
        holding_period — days to hold each quintile portfolio

    Returns:
        DataFrame with quintile returns by date
    """
    # Merge factor with forward returns
    df = momentum_df[['ticker', 'date', factor_col]].copy()
    df = df.dropna(subset=[factor_col])

    ret = returns_df[['ticker', 'date', 'log_return']].copy()

    # Create forward returns: return T+1 to T+holding_period
    # For simplicity with daily data: T+1 return
    ret_forward = ret.copy()
    ret_forward = ret_forward.rename(columns={'log_return': 'forward_return'})
    ret_forward['signal_date'] = ret_forward.groupby('ticker')['date'].shift(holding_period)
    ret_forward = ret_forward.dropna(subset=['signal_date'])
    ret_forward = ret_forward.rename(columns={'signal_date': 'date'})

    merged = df.merge(ret_forward[['ticker', 'date', 'forward_return']], on=['ticker', 'date'])

    if len(merged) == 0:
        logger.warning("No data after merging factor with forward returns")
        return pd.DataFrame()

    # Assign quintiles cross-sectionally on each date
    def assign_quintile(group):
        if len(group.dropna()) < min_stocks_per_quintile * 5:
            return group.assign(quintile=np.nan)
        group = group.copy()
        group['quintile'] = pd.qcut(
            group[factor_col],
            q=5,
            labels=[1, 2, 3, 4, 5],
            duplicates='drop'
        )
        return group

    merged = merged.groupby('date', group_keys=False).apply(assign_quintile)
    merged = merged.dropna(subset=['quintile'])

    # Compute equal-weighted returns for each quintile on each date
    quintile_returns = (
        merged.groupby(['date', 'quintile'])['forward_return']
        .mean()
        .reset_index()
    )

    # Summary statistics
    summary = (
        quintile_returns.groupby('quintile')['forward_return']
        .agg(
            mean_return='mean',
            std_return='std',
            n_obs='count',
            t_stat=lambda x: x.mean() / (x.std() / np.sqrt(len(x)))
        )
        .reset_index()
    )

    # Long-short: Q5 minus Q1
    q5 = summary[summary['quintile'] == 5]['mean_return'].values
    q1 = summary[summary['quintile'] == 1]['mean_return'].values

    if len(q5) > 0 and len(q1) > 0:
        ls_spread = float(q5[0] - q1[0])
        logger.info(f"Long-short spread ({factor_col}): {ls_spread*100:.3f}% per day")

    return quintile_returns, summary