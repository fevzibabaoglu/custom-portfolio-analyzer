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
        shares: List[float],
        withholding_tax_rates: List[float],
        reference_prices: List[float],
        initial_prices: List[float],
        final_prices: List[float],
    ) -> float:
        """Calculate the performance index of the portfolio based on static allocation."""

        if len({
            len(shares),
            len(withholding_tax_rates),
            len(reference_prices),
            len(initial_prices),
            len(final_prices),
        }) != 1:
            raise ValueError("All input lists must have the same length")

        nominator = sum(
            (share * reference) * ((final / initial) * (1 - tax) + tax if final > initial else final / initial)
            for share, tax, reference, initial, final in zip(shares, withholding_tax_rates, reference_prices, initial_prices, final_prices)
        )

        denominator = sum(shares)

        return nominator / denominator
