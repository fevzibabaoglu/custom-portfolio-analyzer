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


class PortfolioPerformance:
    @staticmethod
    def static_allocation_performance_index(
        weights: List[float],
        withholding_tax_rates: List[float],
        initial_prices: List[float],
        final_prices: List[float],
    ) -> float:
        """Calculate the performance index of the portfolio based on static allocation."""

        if len({
            len(weights),
            len(withholding_tax_rates),
            len(initial_prices),
            len(final_prices),
        }) != 1:
            raise ValueError("Weights, withholding tax rates, initial prices, and final prices must have the same amount of elements.")

        nominator = sum(
            weight * ((final / initial) * (1 - tax) + tax if final > initial else final / initial)
            for weight, tax, initial, final in zip(weights, withholding_tax_rates, initial_prices, final_prices)
        )

        denominator = sum(
            weight / initial_price
            for weight, initial_price in zip(weights, initial_prices)
        )

        return nominator / denominator
