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

from data_struct import Asset, ComparisonConfig


class DataLoader:
    def __init__(self, asset_data_path: str, comparison_config_path: str):
        self.assets = Asset.from_csv(asset_data_path)
        self.comparison_config = ComparisonConfig.from_json(comparison_config_path, self.assets)

    def get_assets(self) -> List[Asset]:
        return self.assets

    def get_comparison_config(self) -> ComparisonConfig:
        return self.comparison_config
