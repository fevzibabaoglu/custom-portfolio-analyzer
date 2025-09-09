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
    from .price import Price


from datetime import date
from typing import List, Optional

from .asset import Asset
from utils import DateUtils


class PortfolioAsset:
    def __init__(self, asset: Asset, share: float, order_date: Optional[date] = None):
        self.asset = asset
        self.share = share
        self.order_date = order_date
        self.is_specific = order_date is not None
        self._check_validity()

    def get_asset(self) -> Asset:
        return self.asset

    def get_share(self) -> float:
        return self.share

    def get_order_date(self) -> date:
        return self.order_date

    def set_order_date(self, order_date: date):
        if not self.is_specific:
            available_order_date = next(
                (
                    price.get_date()
                    for price in self.get_asset().get_prices()
                    if price.get_date() >= order_date
                ),
                None,
            )
            self.order_date = available_order_date
            self._check_validity()

    @classmethod
    def from_dict(
        cls,
        data: dict,
        asset_list: List[Asset],
        reference_prices: List[Optional[Price]],
    ) -> 'PortfolioAsset':
        asset_code = data.get('code', None)
        asset, reference_price = next(
            (
                (a, rp)
                for a, rp in zip(asset_list, reference_prices)
                if a.get_code() == asset_code
            ),
            (None, None),
        )

        order_date_str = data.get('order_date', None)
        order_date = (
            DateUtils.parse_date(order_date_str)
            if order_date_str
            else None
        )

        weight = data.get('weight', None)
        share = data.get('share', None)

        if weight is None and share is None:
            raise ValueError(f"Either weight or share must be provided for {asset.get_code()}.")
        if share is None:
            share = cls._calculate_share_from_weight(weight, reference_price)

        return cls(
            asset=asset,
            share=float(share),
            order_date=order_date,
        )

    @staticmethod
    def _calculate_share_from_weight(weight: float, reference_price: Optional[Price]) -> float:
        if reference_price is None:
            raise ValueError("Price on reference date is not available.")
        return weight / reference_price.get_value()

    def _check_validity(self) -> bool:
        if not self.get_asset():
            raise ValueError("Asset cannot be empty.")
        if not isinstance(self.get_asset(), Asset):
            raise ValueError("Asset must be an instance of the Asset class.")
        if self.get_order_date() is not None and not isinstance(self.get_order_date(), date):
            raise ValueError("Order date must be a date object.")
        if self.get_share() is None:
            raise ValueError("Share cannot be None.")
        if not isinstance(self.get_share(), float):
            raise ValueError("Share must be a float number.")
        return True
