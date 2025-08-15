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


# Global Configurations
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


class Main:
    def __init__(
        self,
        default_asset_data_path: str = 'data/asset_data.csv',
        default_config_path: str = 'data/comparison_config.json',
        default_date_format: str = '%d.%m.%Y',
    ):
        self.default_asset_data_path = default_asset_data_path
        self.default_config_path = default_config_path
        self.default_date_format = default_date_format
        self._validate_default_args()
        
        self.args = self.parse_args()
        self._validate_user_args()

        self.configure()

    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Run portfolio performance analysis and chart plotting."
        )
        parser.add_argument(
            '--asset-data-path',
            type=str,
            default=self.default_asset_data_path,
            help='Path to the asset data CSV file',
        )
        parser.add_argument(
            '--config-path',
            type=str,
            default=self.default_config_path,
            help='Path to the portfolio comparison config JSON file',
        )
        parser.add_argument(
            '--date-format',
            type=str,
            default=self.default_date_format,
            help=f'Date format string for displaying dates (default: "{self.default_date_format}")'
        )
        return parser.parse_args()

    def configure(self):
        # Set the date format for classes
        DateUtils.set_date_format(self.args.date_format)

    def run(self):
        loader = DataLoader(
            asset_data_path=self.args.asset_data_path,
            comparison_config_path=self.args.config_path,
        )
        comparison_config = loader.get_comparison_config()

        analyzer_instance = analyzer.Analyzer(comparison_config)
        performance_portfolio_comparisons = analyzer_instance.get_performance_portfolio_comparison_list()

        plotter = ProfitChartPlotter(performance_portfolio_comparisons=performance_portfolio_comparisons)
        plotter.plot_charts()

    def _validate_default_args(self) -> bool:
        if not self.default_asset_data_path:
            raise ValueError("Default asset data path cannot be empty.")
        if not isinstance(self.default_asset_data_path, str):
            raise ValueError("Default asset data path must be a string.")
        if not self.default_config_path:
            raise ValueError("Default config path cannot be empty.")
        if not isinstance(self.default_config_path, str):
            raise ValueError("Default config path must be a string.")
        if not self.default_date_format:
            raise ValueError("Default date format cannot be empty.")
        if not isinstance(self.default_date_format, str):
            raise ValueError("Default date format must be a string.")
        return True

    def _validate_user_args(self) -> bool:
        if not self.args.asset_data_path:
            raise ValueError("Asset data path cannot be empty.")
        if not isinstance(self.args.asset_data_path, str):
            raise ValueError("Asset data path must be a string.")
        if not self.args.config_path:
            raise ValueError("Config path cannot be empty.")
        if not isinstance(self.args.config_path, str):
            raise ValueError("Config path must be a string.")
        if not self.args.date_format:
            raise ValueError("Date format cannot be empty.")
        if not isinstance(self.args.date_format, str):
            raise ValueError("Date format must be a string.")
        return True


if __name__ == '__main__':
    Main(
        default_asset_data_path='data/asset_data.csv',
        default_config_path='data/comparison_config.json',
        default_date_format='%d.%m.%Y',
    ).run()
