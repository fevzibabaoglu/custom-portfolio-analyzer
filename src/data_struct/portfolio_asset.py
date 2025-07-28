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


from .asset import Asset


class PortfolioAsset:
    def __init__(self, asset: Asset, weight: float):
        self.asset = asset
        self.weight = weight
        self._check_validity()

    def get_asset(self) -> Asset:
        return self.asset

    def get_weight(self) -> float:
        return self.weight

    def _check_validity(self) -> bool:
        if not self.get_asset():
            raise ValueError("Asset cannot be empty.")
        if not isinstance(self.get_asset(), Asset):
            raise ValueError("Asset must be an instance of the Asset class.")
        if self.get_weight() is None:
            raise ValueError("Weight cannot be None.")
        if not isinstance(self.get_weight(), float):
            raise ValueError("Weight must be a float number.")
        if not (0 < self.get_weight() <= 1):
            raise ValueError("Weight must be between 0 and 1.")
        return True
