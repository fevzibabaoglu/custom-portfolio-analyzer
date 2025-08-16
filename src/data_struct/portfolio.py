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
    from .date_range import DateRange


from typing import List

from .asset import Asset
from .portfolio_asset import PortfolioAsset
from .price import Price
from analyze import PortfolioPerformance


class Portfolio:
    def __init__(self, title: str, assets: List[PortfolioAsset], is_set_default: bool = False):
        self.title = title
        self.assets = assets
        self._is_set_default = is_set_default
        self._check_validity()

    def get_title(self) -> str:
        return self.title

    def get_assets(self) -> List[PortfolioAsset]:
        return self.assets

    def is_set_default(self) -> bool:
        return self._is_set_default

    def generate_performance_asset(self, date_range: DateRange) -> Asset:
        performance_asset_prices: List[Price] = []

        # Get assets, their weights and withholding tax rates from the portfolio
        asset_data_tuples = [
            (
                asset.get_asset(),
                asset.get_weight(),
                asset.get_asset().get_additional_info().get_withholding_tax_rate(),
            )
            for asset in self.get_assets()
        ]
        assets, weights, withholding_tax_rates = map(list, zip(*asset_data_tuples))

        # Get the price history for each asset over the given date range
        asset_prices_list = [
            asset.get_prices(date_range)
            for asset in assets
        ]

        # Filter each asset's price history to only common dates
        date_sets = [set(p.get_date() for p in prices) for prices in asset_prices_list]
        common_dates = sorted(set.intersection(*date_sets))
        aligned_asset_prices = [
            [p for p in prices if p.get_date() in common_dates]
            for prices in asset_prices_list
        ]

        # Transpose the list to group prices by date
        prices_by_date = list(zip(*aligned_asset_prices))
        initial_prices = prices_by_date[0]

        for prices_on_date in prices_by_date:
            sapi = PortfolioPerformance.static_allocation_performance_index(
                weights=weights,
                withholding_tax_rates=withholding_tax_rates,
                initial_prices=[price.get_value() for price in initial_prices],
                final_prices=[price.get_value() for price in prices_on_date],
            )

            portfolio_performance_price = Price(
                date=prices_on_date[0].get_date(),
                value=sapi,
            )
            performance_asset_prices.append(portfolio_performance_price)

        title = self.get_title()
        portfolio_code = ''.join(word[0].upper() for word in title.split())

        performance_asset = Asset(
            code=portfolio_code,
            name=title,
            prices=performance_asset_prices,
        )
        performance_asset.is_set_default = self.is_set_default()

        return performance_asset

    @classmethod
    def from_dict(cls, data: dict, asset_list: List[Asset]) -> 'Portfolio':
        is_disabled = data.get('disabled', False)
        if is_disabled:
            return None

        title = data.get('title', None)
        is_set_default = data.get('is_set_default', False)

        asset_data = data.get('assets', None)
        assets = [
            PortfolioAsset.from_dict(asset, asset_list)
            for asset in asset_data
        ] if asset_data else None

        return cls(
            title=title,
            assets=assets,
            is_set_default=is_set_default,
        )

    def _check_validity(self) -> bool:
        if not self.get_title():
            raise ValueError("Portfolio title cannot be empty.")
        if not isinstance(self.get_title(), str):
            raise ValueError("Portfolio title must be a string.")
        if not self.get_assets():
            raise ValueError("Assets cannot be empty.")
        if not isinstance(self.get_assets(), list):
            raise ValueError("Assets must be a list.")
        if not all(isinstance(asset, PortfolioAsset) for asset in self.get_assets()):
            raise ValueError("All assets must be instances of the PortfolioAsset class.")
        if self.is_set_default() is None:
            raise ValueError("is_set_default cannot be empty.")
        if not isinstance(self.is_set_default(), bool):
            raise ValueError("is_set_default must be a boolean.")

        total_weight = sum(asset.get_weight() for asset in self.get_assets())
        if total_weight != 1.0:
            raise ValueError(f"Total weight of assets in portfolio '{self.get_title()}' must equal 1.0, but is {total_weight}.")

        return True
