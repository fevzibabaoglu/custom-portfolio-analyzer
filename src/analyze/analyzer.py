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


from typing import List

from .portfolio_performance_generator import PortfolioPerformanceGenerator
from data_struct import PerformancePortfolioComparison, ComparisonConfig


class Analyzer:
    def __init__(self, comparison_config: ComparisonConfig):
        self.comparison_config = comparison_config
        self._check_validity()

        self.performance_portfolio_comparison_list = self.generate_performance_portfolio_comparison_list()

    def get_comparison_config(self) -> ComparisonConfig:
        return self.comparison_config

    def get_performance_portfolio_comparison_list(self) -> List[PerformancePortfolioComparison]:
        return self.performance_portfolio_comparison_list

    def generate_performance_portfolio_comparison_list(self) -> List[PerformancePortfolioComparison]:
        data_ranges = self.get_comparison_config().get_date_ranges()
        portfolios = self.get_comparison_config().get_portfolios()

        performance_portfolio_comparison_list = []

        for date_range in data_ranges:
            performance_assets = []

            for portfolio in portfolios:
                portfolio_performance_generator = PortfolioPerformanceGenerator(
                    portfolio=portfolio,
                    date_range=date_range,
                )
                performance_asset = portfolio_performance_generator.get_portfolio_performance_asset()
                performance_assets.append(performance_asset)

            performance_portfolio_comparison = PerformancePortfolioComparison(
                date_range=date_range,
                performance_assets=performance_assets,
            )
            performance_portfolio_comparison_list.append(performance_portfolio_comparison)

        return performance_portfolio_comparison_list

    def _check_validity(self) -> bool:
        if not self.comparison_config:
            raise ValueError("Comparison config cannot be empty.")
        if not isinstance(self.comparison_config, ComparisonConfig):
            raise ValueError("Comparison config must be an instance of the ComparisonConfig class.")
        return True
