"""
custom-portfolio-analyzer - A tool to model, back-test, and compare the performance of your own custom portfolios.
Copyright (C) 2025  Fevzi Babaoğlu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


import argparse
import logging

from analyze import analyzer
from data_io import DataLoader
from utils import DateUtils
from visualization import ProfitChartPlotter


# Configurations
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


def validate_date_format(fmt: str) -> str:
    """Validate that the date format is usable with strftime/strptime."""
    try:
        DateUtils.get_today().strftime(fmt)
        return fmt
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid date format: {fmt}. Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Run portfolio performance analysis and chart plotting."
    )
    parser.add_argument(
        '--asset-data-path',
        type=str,
        default='data/asset_data.csv',
        help='Path to the asset data CSV file',
    )
    parser.add_argument(
        '--config-path',
        type=str,
        default='data/portfolio_comparison_config.json',
        help='Path to the portfolio comparison config JSON file',
    )
    parser.add_argument(
        '--date-format',
        type=validate_date_format,
        default='%d.%m.%Y',
        help='Date format string for displaying dates (default: "%d.%m.%Y")'
    )
    args = parser.parse_args()

    # Set the date format for classes
    DateUtils.set_date_format(args.date_format)

    loader = DataLoader(
        asset_data_path=args.asset_data_path,
        portfolio_comparison_config_path=args.config_path,
    )
    portfolio_comparisons = loader.get_portfolio_comparisons()

    for portfolio_comparison in portfolio_comparisons:
        logging.info(f"Analyzing portfolio comparison: {portfolio_comparison.get_title()}")

        analyzer_instance = analyzer.Analyzer(portfolio_comparison)
        performance_portfolio_comparisons = analyzer_instance.get_performance_portfolio_comparison_list()

        plotter = ProfitChartPlotter(performance_portfolio_comparisons=performance_portfolio_comparisons)
        plotter.plot_charts()


if __name__ == '__main__':
    main()
