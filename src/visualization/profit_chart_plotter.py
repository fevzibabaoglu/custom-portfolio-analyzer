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


from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from analyze import Analyzer


import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import date

from data_struct import PerformanceReturn
from utils import DateUtils


class ProfitChartPlotter:
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def plot_charts(self):
        for pib in self.analyzer.generate_performance_info_batches():
            date_range = pib['date_range']
            start_date = date_range.get_start_date()
            end_date = date_range.get_end_date()

            # Create the figure and axis
            fig, ax = plt.subplots(figsize=(12, 6))

            # Plot each performance asset
            for performance_info in pib['performance_infos']:
                portfolio_code = performance_info['portfolio_code']
                portfolio_title = performance_info['portfolio_title']
                performance_returns = performance_info['performance_returns']
                is_set_default = performance_info['is_set_default']

                dates = [performance_return.get_date() for performance_return in performance_returns]
                profit_ratios = PerformanceReturn.calculate_profit_ratios(performance_returns)

                default_label = ' [Default]' if is_set_default else ''
                label = f"{portfolio_title} ({portfolio_code}){default_label}"
                ax.plot(dates, profit_ratios, label=label, linewidth=2)

            # Format the plot
            ax.set_title(
                f"Profit Ratios: {DateUtils.format_date(start_date)} to {DateUtils.format_date(end_date)}",
                fontsize=14,
                weight='bold',
            )
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Profit Ratio", fontsize=12)

            ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
            self._configure_date_axis(ax, start_date, end_date)
            ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.5)
            ax.grid(True, which='major', axis='x', linestyle='--', alpha=0.5)

            ax.legend(title="Assets", fontsize=10)
            plt.tight_layout()
            plt.show()

    @staticmethod
    def _configure_date_axis(ax, start_date: date, end_date: date):
        locator = mdates.AutoDateLocator(minticks=3, maxticks=10)
        ax.xaxis.set_major_locator(locator)

        formatter = mdates.ConciseDateFormatter(locator, show_offset=False)
        ax.xaxis.set_major_formatter(formatter)

        ax.format_coord = lambda x, y: f'x={DateUtils.format_date(mdates.num2date(x).date())}, y={y:.3%}'
        ax.set_xlim(start_date, end_date)
        ax.autoscale(enable=True, axis='both', tight=False)
        ax.margins(x=0.01)
