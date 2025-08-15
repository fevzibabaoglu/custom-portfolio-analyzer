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


import pandas as pd
from typing import List, Optional

from .date_range import DateRange
from .price import Price
from utils import DataFrameUtils


class Asset:
    def __init__(self, code: str, name: str, prices: List[Price]):
        self.code = code
        self.name = name
        self.prices = prices
        self._check_validity()

        self.date_range = DateRange(
            start_date=prices[0].get_date(),
            end_date=prices[-1].get_date(),
        )

    def get_code(self) -> str:
        return self.code

    def get_name(self) -> str:
        return self.name

    def get_prices(self, date_range: Optional[DateRange] = None) -> List[Price]:
        if date_range is None:
            return self.prices

        return [
            p for p in self.prices
            if date_range.get_start_date() <= p.get_date() <= date_range.get_end_date()
        ]

    def get_date_range(self) -> DateRange:
        return self.date_range

    @classmethod
    def from_dict(cls, data: dict) -> 'Asset':
        code = data.get("code", None)
        name = data.get("name", None)

        price_dicts = data.get("prices", None)
        prices = [
            Price.from_dict(price)
            for price in price_dicts
        ] if price_dicts else None

        return cls(
            code=code,
            name=name,
            prices=prices,
        )

    @classmethod
    def from_csv(cls, csv_path: str) -> List['Asset']:
        df = pd.read_csv(csv_path, encoding="utf-8")
        df = DataFrameUtils.postprocess_dataframe(df)

        return [
            cls.from_dict(row)
            for row in df.to_dict(orient="records")
        ]

    def _check_validity(self) -> bool:
        if not self.get_code():
            raise ValueError("Asset code cannot be empty.")
        if not isinstance(self.get_code(), str):
            raise ValueError("Asset code must be a string.")
        if not self.get_name():
            raise ValueError("Asset name cannot be empty.")
        if not isinstance(self.get_name(), str):
            raise ValueError("Asset name must be a string.")
        if not self.get_prices():
            raise ValueError("Prices cannot be empty.")
        if not isinstance(self.get_prices(), list):
            raise ValueError("Prices must be a list.")
        if not all(isinstance(price, Price) for price in self.get_prices()):
            raise ValueError("All prices must be instances of the Price class.")
        return True
