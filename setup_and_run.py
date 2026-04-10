#!/usr/bin/env python3
"""
nairobi_alpha — Master Setup Script
=====================================
Run this once to load all data and run the full research agenda.

Usage:
    python setup_and_run.py --data-dir /path/to/mendeley/data
    python setup_and_run.py --data-dir ./data/raw --skip-db

Steps:
    1. Ingest all annual files (2007-2025)
    2. Ingest all individual stock files
    3. Load into PostgreSQL (unless --skip-db)
    4. Run full research agenda
    5. Save results
"""

import sys
import argparse
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('nairobi_alpha.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent))


def main():
    parser = argparse.ArgumentParser(description='Nairobi Alpha Setup')
    parser.add_argument('--data-dir', type=str, required=True,
                        help='Path to Mendeley dataset directory')
    parser.add_argument('--skip-db', action='store_true',
                        help='Skip database operations (research only)')
    parser.add_argument('--annual-only', action='store_true',
                        help='Only ingest annual files, skip individual stocks')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        sys.exit(1)

    logger.info(f"Nairobi Alpha Setup — Data: {data_dir}")

    # ── Step 1: Ingest Annual Files ────────────────────────────────────
    logger.info("\n[STEP 1] Ingesting annual all-stocks files...")
    from src.data.acquisition.ingest import (
        ingest_all_annual_files, ingest_all_individual_files, dataset_summary
    )

    prices, indices, returns = ingest_all_annual_files(data_dir)

    if len(prices) == 0:
        logger.error("No data loaded. Check data directory.")
        sys.exit(1)

    dataset_summary(prices)

    # ── Step 2: Ingest Individual Stock Files ─────────────────────────
    if not args.annual_only:
        logger.info("\n[STEP 2] Ingesting individual stock files...")
        ind_prices, ind_returns = ingest_all_individual_files(data_dir)

        if len(ind_prices) > 0:
            logger.info(f"Individual files: {ind_prices['ticker'].nunique()} stocks")

            # Merge with annual data — individual files may extend history
            # or provide OHLC data not in annual files
            logger.info("Individual stock data loaded separately — "
                       "use for OHLC research and extended history")

    # ── Step 3: Database ───────────────────────────────────────────────
    if not args.skip_db:
        logger.info("\n[STEP 3] Loading into PostgreSQL...")
        try:
            from src.data.storage.database import (
                get_engine, upsert_securities, insert_prices, insert_returns
            )
            engine = get_engine()
            logger.info("Database connection established")

            ticker_to_id = upsert_securities(prices, engine)
            n_prices = insert_prices(prices, ticker_to_id, engine)
            n_returns = insert_returns(returns, ticker_to_id, engine)
            logger.info(f"Inserted: {n_prices:,} price rows, {n_returns:,} return rows")
        except Exception as e:
            logger.warning(f"Database step failed: {e}")
            logger.warning("Continuing with in-memory research...")

    # ── Step 4: Full Research Run ──────────────────────────────────────
    logger.info("\n[STEP 4] Running full research agenda...")
    from src.research.engine import run_full_research

    equities_returns = returns[returns['ticker'].isin(
        prices[prices['security_type'] == 'equity']['ticker'].unique()
    )]

    research_results = run_full_research(prices, equities_returns, indices)

    # ── Step 5: Save Key Results ───────────────────────────────────────
    logger.info("\n[STEP 5] Saving results...")
    output_dir = Path('research/outputs')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Efficiency results
    if 'efficiency' in research_results:
        research_results['efficiency'].to_csv(
            output_dir / 'efficiency_tests.csv', index=False
        )

    # Efficiency by year
    if 'efficiency_by_year' in research_results:
        research_results['efficiency_by_year'].to_csv(
            output_dir / 'efficiency_by_year.csv', index=False
        )

    # Correlation matrix
    if 'correlation' in research_results:
        research_results['correlation'].to_csv(
            output_dir / 'correlation_matrix.csv'
        )

    logger.info(f"Results saved to {output_dir}")
    logger.info("\nNairobi Alpha setup complete.")

    return research_results


if __name__ == '__main__':
    main()