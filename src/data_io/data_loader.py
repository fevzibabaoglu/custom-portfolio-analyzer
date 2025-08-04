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


import ast
import json
import pandas as pd
from typing import List

from data_struct import (
    Asset,
    DateRange,
    DateUtils,
    PortfolioAsset,
    PortfolioComparison,
    Portfolio,
    Price,
)


class DataLoader:
    def __init__(
        self,
        asset_data_path = 'data/asset_data.csv',
        portfolio_comparison_config_path = 'data/portfolio_comparison_config.json',
    ):
        self.asset_data_path = asset_data_path
        self.portfolio_comparison_config_path = portfolio_comparison_config_path

        self.asset_data = self.load_asset_data()
        self.portfolio_comparisons = self.load_portfolio_comparisons()

    def get_asset_data(self) -> List[Asset]:
        return self.asset_data

    def get_portfolio_comparisons(self) -> List[PortfolioComparison]:
        return self.portfolio_comparisons

    def load_asset_data(self) -> List[Asset]:
        assets = []

        df = pd.read_csv(self.asset_data_path, encoding='utf-8')

        for _, row in df.iterrows():
            code = str(row['code']).strip()
            name = str(row['name']).strip()

            price_list_str = row['prices']
            price_list = ast.literal_eval(price_list_str)
            prices = [
                Price(
                    date=DateUtils.parse_date(price_dict['date']),
                    value=price_dict['value'],
                )
                for price_dict in price_list
            ]

            asset = Asset(code=code, name=name, prices=prices)
            assets.append(asset)

        return assets

    def load_portfolio_comparisons(self) -> List[PortfolioComparison]:
        portfolio_comparisons = []

        with open(self.portfolio_comparison_config_path, 'r', encoding='utf-8') as file:
            portfolio_comparison_data = json.load(file)

        for item in portfolio_comparison_data:
            title = item['title']
            date_ranges = self._load_date_ranges(item['date_ranges'])
            portfolios = self._load_portfolios(item['portfolios'])

            portfolio_comparison = PortfolioComparison(
                title=title,
                date_ranges=date_ranges,
                portfolios=portfolios,
            )
            portfolio_comparisons.append(portfolio_comparison)

        return portfolio_comparisons

    def _load_date_ranges(self, date_range_data: List[dict]) -> List[DateRange]:
        date_ranges = []

        for item in date_range_data:
            start_date_str = item['start']
            end_date_str = item['end']

            if start_date_str.lower() == 'today':
                start_date = DateUtils.get_today()
            else:
                start_date = DateUtils.parse_date(start_date_str)

            if end_date_str.lower() == 'today':
                end_date = DateUtils.get_today()
            else:
                end_date = DateUtils.parse_date(end_date_str)

            date_range = DateRange(start_date=start_date, end_date=end_date)
            date_ranges.append(date_range)

        return date_ranges

    def _load_portfolios(self, portfolio_data: List[dict]) -> List[Portfolio]:
        portfolios = []

        for item in portfolio_data:
            title = item['title']
            assets = self._load_portfolio_assets(item['assets'])
            is_set_default = item.get('set_default', False)

            portfolio = Portfolio(title=title, assets=assets, is_set_default=is_set_default)
            portfolios.append(portfolio)

        return portfolios
    
    def _load_portfolio_assets(self, portfolio_asset_data: List[dict]) -> List[PortfolioAsset]:
        portfolio_assets = []

        for item in portfolio_asset_data:
            asset = next(
                (a for a in self.asset_data if a.get_code() == item['code']),
                None
            )
            weight = item.get('weight', None)
            withholding_tax_rate = item.get('withholding_tax_rate', 0.0) # Default to 0.0

            portfolio_asset = PortfolioAsset(asset=asset, weight=weight, withholding_tax_rate=withholding_tax_rate)
            portfolio_assets.append(portfolio_asset)

        return portfolio_assets
