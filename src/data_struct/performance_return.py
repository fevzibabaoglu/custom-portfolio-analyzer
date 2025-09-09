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


from datetime import date
from typing import List


class PerformanceReturn:
    def __init__(
        self,
        date: date,
        return_percentage_raw: float,
        return_percentage_tax_applied: float,
    ):
        self.date = date
        self.return_percentage_raw = return_percentage_raw
        self.return_percentage_tax_applied = return_percentage_tax_applied
        self._check_validity()

    def get_date(self) -> date:
        return self.date

    def get_return_percentage_raw(self) -> float:
        return self.return_percentage_raw

    def get_return_percentage_tax_applied(self) -> float:
        return self.return_percentage_tax_applied

    @staticmethod
    def calculate_profit_ratios(performance_return_list: List["PerformanceReturn"]) -> List[float]:
        return [
            pr.get_return_percentage_tax_applied()
            for pr in performance_return_list
        ]

    def _check_validity(self) -> bool:
        if not self.get_date():
            raise ValueError("Date cannot be empty.")
        if not isinstance(self.get_date(), date):
            raise ValueError("Date must be instance of the date class.")
        if self.get_return_percentage_raw() is None:
            raise ValueError("Return percentage (raw) cannot be empty.")
        if not isinstance(self.get_return_percentage_raw(), float):
            raise ValueError("Return percentage (raw) must be a float number.")
        if self.get_return_percentage_tax_applied() is None:
            raise ValueError("Return percentage (tax applied) cannot be empty.")
        if not isinstance(self.get_return_percentage_tax_applied(), float):
            raise ValueError("Return percentage (tax applied) must be a float number.")
        return True
