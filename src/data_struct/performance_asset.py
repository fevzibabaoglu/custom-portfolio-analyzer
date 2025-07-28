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

from .asset import Asset


class PerformanceAsset:
    def __init__(self, asset: Asset):
        self.asset = asset
        self._check_validity()

        self.profit_ratios = self.calculate_profit_ratios()

    def get_asset(self) -> Asset:
        return self.asset

    def get_profit_ratios(self) -> List[float]:
        return self.profit_ratios

    def calculate_profit_ratios(self) -> List[float]:
        prices = [price.get_value() for price in self.asset.get_prices()]
        initial_price = prices[0]
        return [price / initial_price - 1 for price in prices]

    def _check_validity(self) -> bool:
        if not self.asset:
            raise ValueError("Asset cannot be empty.")
        if not isinstance(self.asset, Asset):
            raise ValueError("Asset must be an instance of the Asset class.")
        return True
