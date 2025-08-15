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
    from data_struct import ComparisonConfig

from typing import Iterator


class Analyzer:
    def __init__(self, comparison_config: ComparisonConfig):
        self.comparison_config = comparison_config

    def generate_performance_asset_batches(self) -> Iterator[dict]:
        data_ranges = self.comparison_config.get_date_ranges()
        portfolios = self.comparison_config.get_portfolios()

        for date_range in data_ranges:
            performance_assets = [
                portfolio.generate_performance_asset(date_range)
                for portfolio in portfolios
            ]

            yield {
                'date_range': date_range,
                'performance_assets': performance_assets,
            }
