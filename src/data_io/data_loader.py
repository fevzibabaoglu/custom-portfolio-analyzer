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
from datetime import datetime
from typing import List

from data_struct import Asset, DateRange, PortfolioAsset, PortfolioComparison, Portfolio, Price


class DataLoader:
    DATE_FORMAT = "%d.%m.%Y"

    @classmethod
    def set_date_format(cls, date_format: str):
        cls.date_format = date_format

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

            price_chart_str = row['price_chart']
            price_chart = ast.literal_eval(price_chart_str)
            prices = [
                Price(
                    datetime.strptime(date, self.DATE_FORMAT).date(),
                    value,
                ) 
                for date, value in price_chart
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
                start_date = datetime.today().date()
            else:
                start_date = datetime.strptime(start_date_str, self.DATE_FORMAT).date()

            if end_date_str.lower() == 'today':
                end_date = datetime.today().date()
            else:
                end_date = datetime.strptime(end_date_str, self.DATE_FORMAT).date()

            date_range = DateRange(start_date=start_date, end_date=end_date)
            date_ranges.append(date_range)

        return date_ranges

    def _load_portfolios(self, portfolio_data: List[dict]) -> List[Portfolio]:
        portfolios = []

        for item in portfolio_data:
            title = item['title']
            assets = self._load_portfolio_assets(item['assets'])

            portfolio = Portfolio(title=title, assets=assets)
            portfolios.append(portfolio)

        return portfolios
    
    def _load_portfolio_assets(self, portfolio_asset_data: List[dict]) -> List[PortfolioAsset]:
        portfolio_assets = []

        for item in portfolio_asset_data:
            asset = next(
                (a for a in self.asset_data if a.get_code() == item['code']),
                None
            )
            weight = item['weight']

            portfolio_asset = PortfolioAsset(asset=asset, weight=weight)
            portfolio_assets.append(portfolio_asset)

        return portfolio_assets
