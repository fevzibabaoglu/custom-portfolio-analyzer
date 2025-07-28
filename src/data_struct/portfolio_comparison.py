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

from .date_range import DateRange
from .portfolio import Portfolio


class PortfolioComparison:
    def __init__(self, title:str,  date_ranges: List[DateRange], portfolios: List[Portfolio]):
        self.title = title
        self.date_ranges = date_ranges
        self.portfolios = portfolios
        self._check_validity()

    def get_title(self) -> str:
        return self.title

    def get_date_ranges(self) -> List[DateRange]:
        return self.date_ranges

    def get_portfolios(self) -> List[Portfolio]:
        return self.portfolios

    def _check_validity(self) -> bool:
        if not self.get_title():
            raise ValueError("Comparison title cannot be empty.")
        if not isinstance(self.get_title(), str):
            raise ValueError("Comparison title must be a string.")
        if not self.get_date_ranges() or len(self.get_date_ranges()) == 0:
            raise ValueError("At least one date range is required for comparison.")
        if not all(isinstance(date_range, DateRange) for date_range in self.get_date_ranges()):
            raise ValueError("All date ranges must be instances of the DateRange class.")
        if not self.get_portfolios() or len(self.get_portfolios()) == 0:
            raise ValueError("At least one portfolio is required for comparison.")
        if not all(isinstance(portfolio, Portfolio) for portfolio in self.get_portfolios()):
            raise ValueError("All portfolios must be instances of the Portfolio class.")

        for portfolio in self.get_portfolios():
            for portfolio_asset in portfolio.get_assets():
                asset = portfolio_asset.get_asset()
                asset_date_range = asset.get_date_range()

                if not any(
                    date_range.get_start_date() >= asset_date_range.get_start_date() and
                    date_range.get_end_date() <= asset_date_range.get_end_date()
                    for date_range in self.get_date_ranges()
                ):
                    raise ValueError(f"Asset '{asset.get_code()}' in portfolio '{portfolio.get_title()}' does not contain data for some dates from the asked date range.")

        return True
