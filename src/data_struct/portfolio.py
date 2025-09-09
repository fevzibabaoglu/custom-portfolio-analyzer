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
from typing import List, Optional

from .asset import Asset
from .portfolio_asset import PortfolioAsset
from .price import Price
from utils import DateUtils


class Portfolio:
    def __init__(
        self,
        title: str,
        assets: List[PortfolioAsset],
        price_reference_date: date,
        is_set_default: bool,
        is_specific: bool,
    ):
        self.title = title
        self.assets = assets
        self.price_reference_date = price_reference_date
        self._is_set_default = is_set_default
        self._is_specific = is_specific
        self._check_validity()

    def get_title(self) -> str:
        return self.title

    def get_assets(self) -> List[PortfolioAsset]:
        return self.assets

    def get_price_reference_date(self) -> date:
        return self.price_reference_date

    def is_set_default(self) -> bool:
        return self._is_set_default

    def is_specific(self) -> bool:
        return self._is_specific

    def set_asset_order_dates(self, order_date: date):
        if not self.is_specific():
            max_first_price_date = max(
                asset.get_asset().get_prices()[0].get_date()
                for asset in self.get_assets()
            )
            min_order_date = max(order_date, max_first_price_date)

            for asset in self.get_assets():
                asset.set_order_date(min_order_date)

    @classmethod
    def from_dict(cls, data: dict, asset_list: List[Asset]) -> 'Portfolio':
        is_disabled = data.get('disabled', False)
        if is_disabled:
            return None

        title = data.get('title', None)
        is_set_default = data.get('is_set_default', False)

        price_reference_date_str = data.get('price_reference_date', None)
        price_reference_date = (
            DateUtils.parse_date(price_reference_date_str)
            if price_reference_date_str
            else min(
                asset.get_prices()[-1].get_date()
                for asset in asset_list
            )
        )
        reference_prices = cls._get_reference_prices(price_reference_date, asset_list)

        asset_data = data.get('assets', None)
        assets = [
            PortfolioAsset.from_dict(asset, asset_list, reference_prices)
            for asset in asset_data
        ] if asset_data else None

        are_assets_specific = [asset.is_specific for asset in assets]
        if any(are_assets_specific) and not all(are_assets_specific):
            raise ValueError("Cannot set order_date for portfolio with mixed specific and non-specific assets.")

        return cls(
            title=title,
            assets=assets,
            price_reference_date=price_reference_date,
            is_set_default=is_set_default,
            is_specific=all(are_assets_specific),
        )

    @staticmethod
    def _get_reference_prices(price_reference_date: date, asset_list: List[Asset]) -> List[Optional[Price]]:
        reference_prices = [
            asset.get_price(price_reference_date)
            for asset in asset_list
        ]
        return reference_prices

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
        if not self.get_price_reference_date():
            raise ValueError("price_reference_date cannot be empty.")
        if not isinstance(self.get_price_reference_date(), date):
            raise ValueError("price_reference_date must be a date object.")
        if self.is_set_default() is None:
            raise ValueError("is_set_default cannot be empty.")
        if not isinstance(self.is_set_default(), bool):
            raise ValueError("is_set_default must be a boolean.")
        return True
