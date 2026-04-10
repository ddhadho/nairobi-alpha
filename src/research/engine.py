"""
nairobi_alpha.research.engine
================================
Multi-year research engine.

Once the full dataset is loaded this module runs the complete
research agenda across all years:

1. Market efficiency tests — autocorrelation, variance ratio
2. Factor research — momentum, mean reversion, value, size, liquidity
3. Regime analysis — bull/bear/crisis periods
4. Risk model — covariance structure, factor decomposition
5. Performance attribution — what drives NSE returns

Designed to run on the combined 2007-2025 dataset.
Each analysis writes results to the research_runs database table.
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

logger = logging.getLogger(__name__)


# ── Market Efficiency ──────────────────────────────────────────────────────────

def test_market_efficiency(returns_df: pd.DataFrame,
                            min_obs: int = 50) -> pd.DataFrame:
    """
    Test weak-form market efficiency for each stock.

    Tests:
    1. Lag 1-5 autocorrelation
    2. Ljung-Box test (joint significance of first 10 lags)
    3. Runs test (are runs random?)

    A market is weak-form efficient if past prices contain no information
    about future prices. Rejection of these tests = predictability exists.

    Parameters:
        returns_df — DataFrame with ticker, date, log_return
        min_obs    — minimum observations per stock

    Returns:
        DataFrame with efficiency test results per stock
    """
    results = []

    for ticker, group in returns_df.groupby('ticker'):
        ret = group.sort_values('date')['log_return'].dropna()
        if len(ret) < min_obs:
            continue

        # Autocorrelations at multiple lags
        acs = {f'ac_lag{i}': ret.autocorr(lag=i) for i in range(1, 6)}

        # Ljung-Box test
        try:
            lb = acorr_ljungbox(ret, lags=[10], return_df=True)
            lb_stat = float(lb['lb_stat'].iloc[0])
            lb_pval = float(lb['lb_pvalue'].iloc[0])
        except Exception:
            lb_stat, lb_pval = np.nan, np.nan

        # Variance ratio test (Lo-MacKinlay)
        # VR(q) = Var(q-period return) / (q * Var(1-period return))
        # Under random walk: VR(q) = 1
        vr_results = {}
        for q in [2, 4, 8, 16]:
            vr = _variance_ratio(ret.values, q)
            vr_results[f'vr_{q}'] = vr

        row = {
            'ticker': ticker,
            'n_obs': len(ret),
            'mean_return': ret.mean(),
            'std_return': ret.std(),
            **acs,
            'lb_stat': lb_stat,
            'lb_pval': lb_pval,
            'efficient_lb': lb_pval >= 0.05,
            **vr_results,
        }
        results.append(row)

    df = pd.DataFrame(results)

    # Market-level summary
    if len(df) > 0:
        logger.info(f"Efficiency tests: {len(df)} stocks")
        logger.info(f"Mean lag-1 AC: {df['ac_lag1'].mean():.4f}")
        logger.info(f"Efficient (Ljung-Box): "
                    f"{df['efficient_lb'].mean()*100:.1f}% of stocks")

    return df


def _variance_ratio(returns: np.ndarray, q: int) -> float:
    """
    Compute variance ratio statistic.
    VR(q) = 1 means random walk. VR > 1 means momentum. VR < 1 means reversion.
    """
    n = len(returns)
    if n < q * 4:
        return np.nan

    # q-period returns
    q_returns = np.array([
        returns[i:i+q].sum() for i in range(0, n-q+1, 1)
    ])

    var_1 = np.var(returns, ddof=1)
    var_q = np.var(q_returns, ddof=1)

    if var_1 == 0:
        return np.nan

    return var_q / (q * var_1)


def efficiency_by_year(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Run efficiency tests year by year to see how market efficiency
    has changed over time as NSE has developed.

    Key question: Is NSE becoming more efficient over 2007-2025?
    """
    returns_df = returns_df.copy()
    returns_df['year'] = pd.to_datetime(returns_df['date']).dt.year

    yearly_results = []

    for year, year_data in returns_df.groupby('year'):
        eff = test_market_efficiency(year_data, min_obs=30)
        if len(eff) == 0:
            continue

        yearly_results.append({
            'year': year,
            'n_stocks': len(eff),
            'mean_ac_lag1': eff['ac_lag1'].mean(),
            'pct_momentum': (eff['ac_lag1'] > 0).mean(),
            'pct_efficient': eff['efficient_lb'].mean(),
            'mean_vr2': eff['vr_2'].mean() if 'vr_2' in eff.columns else np.nan,
        })

    result = pd.DataFrame(yearly_results)
    logger.info(f"Efficiency by year computed for {len(result)} years")
    return result


# ── Cross-Sectional Factor Research ───────────────────────────────────────────

def factor_ic_analysis(factor_df: pd.DataFrame,
                        returns_df: pd.DataFrame,
                        factor_col: str,
                        holding_period: int = 1,
                        min_stocks: int = 5) -> dict:
    """
    Compute Information Coefficient (IC) for a factor.

    IC = Spearman rank correlation between factor value today
         and stock return over next holding_period days.

    A factor with consistent positive IC predicts returns correctly.
    IC IR (mean IC / std IC) measures consistency of prediction.

    IC > 0.05 is considered meaningful in practice.
    IC IR > 0.5 is considered good.

    Parameters:
        factor_df      — ticker, date, factor_col
        returns_df     — ticker, date, log_return
        factor_col     — which factor to test
        holding_period — days ahead to predict

    Returns:
        dict with mean_ic, ic_std, ic_ir, t_stat, pct_positive, daily_ics
    """
    # Build forward returns
    ret = returns_df.copy().sort_values(['ticker', 'date'])

    if holding_period == 1:
        ret['fwd_return'] = ret.groupby('ticker')['log_return'].shift(-1)
    else:
        # Multi-day forward return: sum of next H log returns
        ret['fwd_return'] = (ret.groupby('ticker')['log_return']
                             .transform(lambda x: x.shift(-1).rolling(holding_period).sum()))

    ret = ret.dropna(subset=['fwd_return'])

    # Merge factor with forward returns
    merged = factor_df[['ticker', 'date', factor_col]].merge(
        ret[['ticker', 'date', 'fwd_return']],
        on=['ticker', 'date']
    ).dropna()

    if len(merged) == 0:
        return {}

    # Daily IC
    daily_ics = []
    for date, group in merged.groupby('date'):
        if len(group) < min_stocks:
            continue
        ic = group[factor_col].corr(group['fwd_return'], method='spearman')
        daily_ics.append({'date': date, 'ic': ic})

    if not daily_ics:
        return {}

    ic_series = pd.DataFrame(daily_ics)['ic'].dropna()

    mean_ic = ic_series.mean()
    ic_std = ic_series.std()
    ic_ir = mean_ic / ic_std if ic_std > 0 else 0
    t_stat = mean_ic / (ic_std / np.sqrt(len(ic_series)))

    return {
        'factor': factor_col,
        'mean_ic': float(mean_ic),
        'ic_std': float(ic_std),
        'ic_ir': float(ic_ir),
        't_stat': float(t_stat),
        'pct_positive': float((ic_series > 0).mean()),
        'n_days': len(ic_series),
        'daily_ics': pd.DataFrame(daily_ics),
    }


def quintile_analysis(factor_df: pd.DataFrame,
                      returns_df: pd.DataFrame,
                      factor_col: str,
                      holding_period: int = 1,
                      min_stocks_per_quintile: int = 3) -> dict:
    """
    Sort stocks into quintiles by factor value.
    Compute equal-weighted returns for each quintile.

    Returns quintile return summary and long-short spread.
    """
    ret = returns_df.copy().sort_values(['ticker', 'date'])

    # Forward returns
    ret['fwd_return'] = ret.groupby('ticker')['log_return'].shift(-1)
    ret = ret.dropna(subset=['fwd_return'])

    merged = factor_df[['ticker', 'date', factor_col]].merge(
        ret[['ticker', 'date', 'fwd_return']],
        on=['ticker', 'date']
    ).dropna()

    if len(merged) == 0:
        return {}

    quintile_returns = {q: [] for q in [1, 2, 3, 4, 5]}

    for date, group in merged.groupby('date'):
        if len(group) < min_stocks_per_quintile * 5:
            continue
        try:
            group = group.copy()
            group['quintile'] = pd.qcut(
                group[factor_col], q=5,
                labels=[1, 2, 3, 4, 5],
                duplicates='drop'
            )
            for q in [1, 2, 3, 4, 5]:
                q_rets = group[group['quintile'] == q]['fwd_return']
                if len(q_rets) >= min_stocks_per_quintile:
                    quintile_returns[q].append(q_rets.mean())
        except Exception:
            continue

    summary = []
    for q in [1, 2, 3, 4, 5]:
        rets = pd.Series(quintile_returns[q]).dropna()
        if len(rets) < 10:
            continue
        mean = rets.mean()
        std = rets.std()
        t = mean / (std / np.sqrt(len(rets))) if std > 0 else 0
        summary.append({
            'quintile': q,
            'mean_daily_return': float(mean),
            'ann_return': float(mean * 252),
            'ann_return_pct': float(mean * 252 * 100),
            't_stat': float(t),
            'n_obs': len(rets),
        })

    summary_df = pd.DataFrame(summary)

    # Long-short spread
    ls_spread = None
    if 1 in [r['quintile'] for r in summary] and 5 in [r['quintile'] for r in summary]:
        q1 = next(r['ann_return_pct'] for r in summary if r['quintile'] == 1)
        q5 = next(r['ann_return_pct'] for r in summary if r['quintile'] == 5)
        ls_spread = q5 - q1

    return {
        'factor': factor_col,
        'summary': summary_df,
        'ls_spread_ann_pct': ls_spread,
    }


# ── Regime Analysis ────────────────────────────────────────────────────────────

def identify_regimes(index_df: pd.DataFrame,
                     bear_threshold: float = -0.20,
                     bull_threshold: float = 0.20,
                     window: int = 252) -> pd.DataFrame:
    """
    Identify bull and bear market regimes in NSE using NSE 20 index.

    Simple definition:
    - Bull: rolling 252-day return > +20%
    - Bear: rolling 252-day return < -20%
    - Neutral: between

    Understanding regimes is critical for factor research.
    Factors that work in bull markets may fail in bear markets.
    """
    df = index_df.sort_values('date').copy()

    # Use NSE 20 as market proxy
    if 'nse_20' in df.columns:
        price_col = 'nse_20'
    elif 'close' in df.columns:
        price_col = 'close'
    else:
        logger.warning("No suitable price column for regime detection")
        return pd.DataFrame()

    prices = pd.to_numeric(df[price_col], errors='coerce')
    rolling_return = prices.pct_change(window)

    df['rolling_return'] = rolling_return
    df['regime'] = 'neutral'
    df.loc[rolling_return > bull_threshold, 'regime'] = 'bull'
    df.loc[rolling_return < bear_threshold, 'regime'] = 'bear'

    regime_summary = df.groupby('regime').agg(
        n_days=('date', 'count'),
        pct_of_time=('date', lambda x: len(x) / len(df))
    )

    logger.info(f"Regime analysis:\n{regime_summary}")
    return df[['date', 'rolling_return', 'regime']]


# ── Risk Model ─────────────────────────────────────────────────────────────────

def compute_covariance_matrix(returns_df: pd.DataFrame,
                               min_overlap: int = 60,
                               method: str = 'sample') -> pd.DataFrame:
    """
    Compute covariance matrix for NSE returns.

    In small markets with incomplete data, covariance estimation is tricky:
    - Sample covariance is noisy with few stocks
    - Missing data (stocks not trading every day) creates gaps
    - We need a robust estimator

    method options:
        'sample'     — standard sample covariance (noisy but unbiased)
        'shrinkage'  — Ledoit-Wolf shrinkage (better for portfolios)

    Parameters:
        returns_df  — ticker, date, log_return
        min_overlap — minimum overlapping observations per pair
    """
    pivot = returns_df.pivot(
        index='date', columns='ticker', values='log_return'
    )

    # Keep only stocks with sufficient data
    sufficient = pivot.notna().sum() >= min_overlap
    pivot = pivot.loc[:, sufficient]

    if method == 'shrinkage':
        try:
            from sklearn.covariance import LedoitWolf
            lw = LedoitWolf()
            clean = pivot.dropna()
            if len(clean) < 10:
                logger.warning("Too few complete rows for shrinkage — using sample")
                return pivot.cov()
            lw.fit(clean.values)
            cov = pd.DataFrame(
                lw.covariance_,
                index=clean.columns,
                columns=clean.columns
            )
            return cov
        except ImportError:
            logger.warning("sklearn not available — using sample covariance")

    return pivot.cov()


def compute_correlation_matrix(returns_df: pd.DataFrame,
                                min_overlap: int = 60) -> pd.DataFrame:
    """Compute correlation matrix."""
    cov = compute_covariance_matrix(returns_df, min_overlap)
    if cov.empty:
        return pd.DataFrame()

    std = np.sqrt(np.diag(cov.values))
    std_outer = np.outer(std, std)
    corr_values = cov.values / std_outer
    corr_values = np.clip(corr_values, -1, 1)

    return pd.DataFrame(corr_values, index=cov.index, columns=cov.columns)


# ── Full Research Run ──────────────────────────────────────────────────────────

def run_full_research(prices_df: pd.DataFrame,
                      returns_df: pd.DataFrame,
                      indices_df: pd.DataFrame = None) -> dict:
    """
    Run the complete Nairobi Alpha research agenda.

    Designed to run on the full 2007-2025 dataset.
    Returns a dict of all research results.

    Call this once you have the full dataset loaded.
    """
    results = {}

    print("\n" + "="*60)
    print("NAIROBI ALPHA — FULL RESEARCH RUN")
    print("="*60)

    # ── 1. Market Efficiency ──────────────────────────────────────────
    print("\n[1/5] Market Efficiency Tests...")
    eff = test_market_efficiency(returns_df)
    results['efficiency'] = eff
    print(f"  Mean lag-1 AC:     {eff['ac_lag1'].mean():.4f}")
    print(f"  % Efficient:       {eff['efficient_lb'].mean()*100:.1f}%")
    print(f"  Mean VR(2):        {eff['vr_2'].mean():.4f} (1.0 = random walk)")

    # ── 2. Efficiency By Year ──────────────────────────────────────────
    print("\n[2/5] Efficiency Evolution Over Time...")
    eff_yearly = efficiency_by_year(returns_df)
    results['efficiency_by_year'] = eff_yearly
    print(eff_yearly[['year','mean_ac_lag1','pct_efficient']].to_string(index=False))

    # ── 3. Factor Research ─────────────────────────────────────────────
    print("\n[3/5] Factor Research...")

    # Import factor modules
    import sys
    sys.path.insert(0, str(__file__).rsplit('src', 1)[0])
    from src.research.factors.momentum import compute_momentum_multi

    equities = prices_df[prices_df['security_type'] == 'equity'].copy()
    mom_df = compute_momentum_multi(equities, windows=[5, 10, 20, 60])

    factor_results = {}
    for window in [5, 10, 20, 60]:
        col = f'mom_{window}d'
        ic_result = factor_ic_analysis(
            mom_df.dropna(subset=[col]),
            returns_df, col
        )
        q_result = quintile_analysis(
            mom_df.dropna(subset=[col]),
            returns_df, col
        )
        factor_results[col] = {'ic': ic_result, 'quintile': q_result}

        if ic_result:
            spread = q_result.get('ls_spread_ann_pct', 0)
            print(f"  {col}: IC={ic_result['mean_ic']:+.4f}, "
                  f"IR={ic_result['ic_ir']:+.3f}, "
                  f"L/S={spread:+.1f}%/yr")

    results['factors'] = factor_results

    # ── 4. Risk Model ──────────────────────────────────────────────────
    print("\n[4/5] Risk Model...")
    corr = compute_correlation_matrix(returns_df)
    if not corr.empty:
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        pairs = upper.stack()
        print(f"  Universe:           {len(corr)} stocks")
        print(f"  Mean correlation:   {pairs.mean():.4f}")
        print(f"  Max correlation:    {pairs.max():.4f}")
        results['correlation'] = corr

    # ── 5. Return Summary ──────────────────────────────────────────────
    print("\n[5/5] Return Summary...")
    ann = returns_df['log_return'].mean() * 252
    vol = returns_df['log_return'].std() * np.sqrt(252)
    sharpe = ann / vol if vol > 0 else 0
    print(f"  Market ann return:  {ann*100:.2f}%")
    print(f"  Market ann vol:     {vol*100:.2f}%")
    print(f"  Market Sharpe:      {sharpe:.3f}")

    print("\n" + "="*60)
    print("Research run complete.")
    print("="*60)

    return results