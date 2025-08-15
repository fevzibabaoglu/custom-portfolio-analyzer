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

from utils import DateUtils


class ProfitChartPlotter:
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def plot_charts(self):
        for pab in self.analyzer.generate_performance_asset_batches():
            date_range = pab['date_range']
            start_date = date_range.get_start_date()
            end_date = date_range.get_end_date()

            # Create the figure and axis
            fig, ax = plt.subplots(figsize=(12, 6))

            # Plot each performance asset
            for asset in pab['performance_assets']:
                prices = asset.get_prices(date_range)
                is_set_default = asset.is_set_default if hasattr(asset, 'is_set_default') else False

                dates = [price.get_date() for price in prices]
                profit_ratios = asset.calculate_profit_ratios()

                label = f"{asset.get_name()} ({asset.get_code()}){' [Default]' if is_set_default else ''}"
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

            # Format x-axis ticks
            ax.xaxis.set_major_formatter(mdates.DateFormatter(DateUtils.get_date_format()))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())

            ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.5)
            ax.legend(title="Assets", fontsize=10)
            plt.tight_layout()
            plt.show()
