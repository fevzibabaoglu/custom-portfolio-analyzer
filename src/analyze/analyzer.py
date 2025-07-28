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
from data_struct import PerformancePortfolioComparison, PortfolioComparison


class Analyzer:
    def __init__(self, portfolio_comparison: PortfolioComparison):
        self.portfolio_comparison = portfolio_comparison
        self._check_validity()

        self.performance_portfolio_comparison_list = self.generate_performance_portfolio_comparison_list()

    def get_portfolio_comparison(self) -> PortfolioComparison:
        return self.portfolio_comparison

    def get_performance_portfolio_comparison_list(self) -> List[PerformancePortfolioComparison]:
        return self.performance_portfolio_comparison_list

    def generate_performance_portfolio_comparison_list(self) -> List[PerformancePortfolioComparison]:
        data_ranges = self.portfolio_comparison.get_date_ranges()
        portfolios = self.portfolio_comparison.get_portfolios()

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
        if not self.portfolio_comparison:
            raise ValueError("Portfolio comparison cannot be empty.")
        if not isinstance(self.portfolio_comparison, PortfolioComparison):
            raise ValueError("Portfolio comparison must be an instance of the PortfolioComparison class.")
        return True
