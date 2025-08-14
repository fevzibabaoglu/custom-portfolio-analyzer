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


import logging
import numpy as np
from typing import List

from .date_range import DateRange
from .performance_asset import PerformanceAsset
from utils import DateUtils


class PerformancePortfolioComparison:
    def __init__(self, date_range: DateRange, performance_assets: List[PerformanceAsset]):
        self.date_range = date_range
        self.performance_assets = performance_assets
        self._check_validity()
        self._post_process()

    def get_date_range(self) -> DateRange:
        return self.date_range

    def get_performance_assets(self) -> List[PerformanceAsset]:
        return self.performance_assets

    def _check_validity(self) -> bool:
        if not self.date_range:
            raise ValueError("Date range cannot be empty.")
        if not isinstance(self.date_range, DateRange):
            raise ValueError("Date range must be an instance of the DateRange class.")
        if not self.performance_assets:
            raise ValueError("Performance assets cannot be empty.")
        if not isinstance(self.performance_assets, list):
            raise ValueError("Performance assets must be a list.")
        if not all(isinstance(asset, PerformanceAsset) for asset in self.performance_assets):
            raise ValueError("All performance assets must be instances of the PerformanceAsset class.")
        return True

    def _post_process(self):
        # Adjust the date range based on the assets' date ranges
        for performance_asset in self.get_performance_assets():
            asset = performance_asset.get_asset()
            asset_date_range = asset.get_date_range()

            comparison_start_date = self.get_date_range().get_start_date()
            start_date = max(comparison_start_date, asset_date_range.get_start_date())
            if start_date != comparison_start_date:
                logging.info(
                    f"Adjusting start date for {asset.get_code()} "
                    f"from {DateUtils.format_date(comparison_start_date)} "
                    f"to {DateUtils.format_date(start_date)}"
                )
                self.get_date_range().set_start_date(start_date)

            comparison_end_date = self.get_date_range().get_end_date()
            end_date = min(comparison_end_date, asset_date_range.get_end_date())
            if end_date != comparison_end_date:
                logging.info(
                    f"Adjusting end date for {asset.get_code()} "
                    f"from {DateUtils.format_date(comparison_end_date)} "
                    f"to {DateUtils.format_date(end_date)}"
                )
                self.get_date_range().set_end_date(end_date)

        # Compare with the default portfolio
        default_performance_asset = next((
            performance_asset for performance_asset in self.get_performance_assets()
            if performance_asset.is_set_default()
        ), None)
        if default_performance_asset:
            default_profit_ratios = default_performance_asset.get_profit_ratios()

            for performance_asset in self.get_performance_assets():
                compared_profit_ratios = np.subtract(
                    performance_asset.get_profit_ratios(),
                    default_profit_ratios,
                ).tolist()
                performance_asset.set_profit_ratios(compared_profit_ratios)
