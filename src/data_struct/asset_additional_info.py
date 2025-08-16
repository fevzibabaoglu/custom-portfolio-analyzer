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


class AssetAdditionalInfo:
    """Additional fund information not found in the main asset data file."""

    def __init__(self, withholding_tax_rate: float):
        self.withholding_tax_rate = withholding_tax_rate
        self._check_validity()

    def get_withholding_tax_rate(self) -> float:
        return self.withholding_tax_rate

    @classmethod
    def from_dict(cls, data: dict) -> 'AssetAdditionalInfo':
        withholding_tax_rate = data.get("withholding_tax_rate", 0.0)
        return cls(
            withholding_tax_rate=withholding_tax_rate,
        )

    def _check_validity(self):
        if self.get_withholding_tax_rate() is None:
            raise ValueError("Withholding tax rate cannot be empty.")
        if not isinstance(self.get_withholding_tax_rate(), float):
            raise ValueError("Withholding tax rate must be a float number.")
        if self.get_withholding_tax_rate() < 0:
            raise ValueError("Withholding tax rate must be non-negative.")
