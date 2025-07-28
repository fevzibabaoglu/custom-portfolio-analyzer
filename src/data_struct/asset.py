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
from .price import Price


class Asset:
    def __init__(self, code: str, name: str, prices: List[Price]):
        self.code = code
        self.name = name
        self.prices = prices

    def get_code(self) -> str:
        return self.code

    def get_name(self) -> str:
        return self.name

    def get_prices(self, date_range: DateRange) -> List[Price]:
        return [
            p for p in self.prices
            if date_range.get_start_date() <= p.get_date() <= date_range.get_end_date()
        ]
