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

from .portfolio_asset import PortfolioAsset


class Portfolio:
    def __init__(self, title: str, start_date: date, end_date: date, assets: List[PortfolioAsset]):
        self.title: str = title
        self.start_date = start_date
        self.end_date = end_date
        self.assets = assets
        self._check_validity()

    def get_title(self) -> str:
        return self.title

    def get_start_date(self) -> date:
        return self.start_date

    def get_end_date(self) -> date:
        return self.end_date

    def get_assets(self) -> List[PortfolioAsset]:
        return self.assets

    def _check_validity(self) -> bool:
        if self.get_start_date() >= self.get_end_date():
            raise ValueError("Start date must be before end date.")

        total_weight = sum(asset.get_weight() for asset in self.get_assets())
        if total_weight != 1.0:
            raise ValueError(f"Total weight of assets in portfolio '{self.get_title()}' must equal 1.0, but is {total_weight}.")

        return True
