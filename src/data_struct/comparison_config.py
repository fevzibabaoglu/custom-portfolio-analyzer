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
    from .asset import Asset

import json
from typing import List

from .date_range import DateRange
from .portfolio import Portfolio


class ComparisonConfig:
    def __init__(self, date_ranges: List[DateRange], portfolios: List[Portfolio]):
        self.date_ranges = date_ranges
        self.portfolios = portfolios
        self._check_validity()

    def get_date_ranges(self) -> List[DateRange]:
        return self.date_ranges

    def get_portfolios(self) -> List[Portfolio]:
        return self.portfolios

    @classmethod
    def from_dict(cls, data: dict, asset_list: List[Asset]) -> 'ComparisonConfig':
        date_ranges_data = data.get('date_ranges', None)
        date_ranges = [
            DateRange.from_dict(item)
            for item in date_ranges_data
        ] if date_ranges_data else None

        portfolios_data = data.get('portfolios', None)
        portfolios = [
            Portfolio.from_dict(item, asset_list)
            for item in portfolios_data
        ] if portfolios_data else None

        return cls(date_ranges=date_ranges, portfolios=portfolios)

    @classmethod
    def from_json(cls, json_path: str, asset_list: List[Asset]) -> 'ComparisonConfig':
        with open(json_path, 'r', encoding='utf-8') as file:
            comparison_data = json.load(file)
        return cls.from_dict(comparison_data, asset_list)

    def _check_validity(self) -> bool:
        if not self.get_date_ranges():
            raise ValueError("Date ranges cannot be empty.")
        if not isinstance(self.get_date_ranges(), list):
            raise ValueError("Date ranges must be a list.")
        if not all(isinstance(date_range, DateRange) for date_range in self.get_date_ranges()):
            raise ValueError("All date ranges must be instances of the DateRange class.")
        if not self.get_portfolios():
            raise ValueError("Portfolios cannot be empty.")
        if not isinstance(self.get_portfolios(), list):
            raise ValueError("Portfolios must be a list.")
        if not all(isinstance(portfolio, Portfolio) for portfolio in self.get_portfolios()):
            raise ValueError("All portfolios must be instances of the Portfolio class.")
        if sum(p.is_set_default() for p in self.get_portfolios()) > 1:
            raise ValueError("Only one portfolio can be set as default.")
        return True
