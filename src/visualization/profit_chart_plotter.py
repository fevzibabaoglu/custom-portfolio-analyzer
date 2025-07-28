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


import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import PercentFormatter
from typing import List

from data_struct import PerformancePortfolioComparison


class ProfitChartPlotter:
    date_format = "%d.%m.%Y"

    @classmethod
    def set_date_format(cls, date_format: str):
        cls.date_format = date_format

    def __init__(self, performance_portfolio_comparisons: List[PerformancePortfolioComparison]):
        self.performance_portfolio_comparisons = performance_portfolio_comparisons
        self._check_validity()

    def plot_charts(self):
        for ppc in self.performance_portfolio_comparisons:
            date_range = ppc.get_date_range()
            start_date = date_range.get_start_date()
            end_date = date_range.get_end_date()

            # Create the figure and axis
            fig, ax = plt.subplots(figsize=(12, 6))

            # Plot each performance asset
            for performance_asset in ppc.get_performance_assets():
                asset = performance_asset.get_asset()
                prices = asset.get_prices(date_range)

                dates = [price.get_date() for price in prices]
                profit_ratios = performance_asset.get_profit_ratios()

                label = f"{asset.get_name()} ({asset.get_code()})"
                ax.plot(dates, profit_ratios, label=label, linewidth=2)

            # Format the plot
            ax.set_title(
                f"Profit Ratios: {start_date.strftime(self.date_format)} to {end_date.strftime(self.date_format)}",
                fontsize=14,
                weight='bold',
            )
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Profit Ratio", fontsize=12)
            ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

            # Format x-axis ticks as dd.mm.yyyy
            ax.xaxis.set_major_formatter(DateFormatter(self.date_format))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())

            ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.5)
            ax.legend(title="Assets", loc='upper left', fontsize=10)
            plt.tight_layout()
            plt.show()

    def _check_validity(self):
        if not self.performance_portfolio_comparisons:
            raise ValueError("Performance portfolio comparisons cannot be empty.")
        if not isinstance(self.performance_portfolio_comparisons, list):
            raise ValueError("Performance portfolio comparisons must be a list.")
        if not all(isinstance(ppc, PerformancePortfolioComparison) for ppc in self.performance_portfolio_comparisons):
            raise ValueError("All items in the performance portfolio comparisons must be instances of PerformancePortfolioComparison.")
