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

from data_struct import PerformanceAsset, Asset, DateRange, Portfolio, Price


class PortfolioPerformanceGenerator:
    def __init__(self, portfolio: Portfolio, date_range: DateRange):
        self.portfolio = portfolio
        self.date_range = date_range
        self._check_validity()

        self.portfolio_performance_asset = self.generate_performance_asset()

    def get_portfolio_performance_asset(self) -> PerformanceAsset:
        return self.portfolio_performance_asset

    def generate_performance_asset(self) -> PerformanceAsset:
        portfolio_performance_prices: List[Price] = []

        # Get assets and their weights from the portfolio
        asset_weight_tuples = [
            (asset.get_asset(), asset.get_weight())
            for asset in self.portfolio.get_assets()
        ]
        assets, weights = map(list, zip(*asset_weight_tuples))

        # Get the price history for each asset over the given date range
        asset_prices_list = [
            asset.get_prices(self.date_range)
            for asset in assets
        ]

        # Transpose the list to group prices by date
        prices_by_date = list(zip(*asset_prices_list))
        initial_prices = prices_by_date[0]

        for prices_on_date in prices_by_date:
            sapi = self._static_allocation_performance_index(
                weights=weights,
                initial_prices=[price.get_value() for price in initial_prices],
                final_prices=[price.get_value() for price in prices_on_date]
            )

            portfolio_performance_price = Price(
                date=prices_on_date[0].get_date(),
                value=sapi,
            )
            portfolio_performance_prices.append(portfolio_performance_price)

        title = self.portfolio.get_title()
        portfolio_code = ''.join(word[0].upper() for word in title.split())
        portfolio_performance_asset = Asset(
            code=portfolio_code,
            name=title,
            prices=portfolio_performance_prices,
        )

        return PerformanceAsset(
            asset=portfolio_performance_asset,
            is_set_default=self.portfolio.is_set_default(),
        )

    def _static_allocation_performance_index(
        self,
        weights: List[float],
        initial_prices: List[float],
        final_prices: List[float]
    ) -> float:
        """Calculate the performance index of the portfolio based on static allocation."""
        if len(weights) != len(initial_prices) or len(weights) != len(final_prices):
            raise ValueError("Weights, initial prices, and final prices must have the same amount of elements.")

        nominator = sum(
            weight * final_price / initial_price
            for weight, initial_price, final_price in zip(weights, initial_prices, final_prices)
        )

        denominator = sum(
            weight / initial_price
            for weight, initial_price in zip(weights, initial_prices)
        )

        return nominator / denominator

    def _check_validity(self) -> bool:
        if not self.portfolio:
            raise ValueError("Portfolio cannot be empty.")
        if not isinstance(self.portfolio, Portfolio):
            raise ValueError("Portfolio must be an instance of the Portfolio class.")
        if not self.date_range:
            raise ValueError("Date range cannot be empty.")
        if not isinstance(self.date_range, DateRange):
            raise ValueError("Date range must be an instance of the DateRange class.")
        return True
