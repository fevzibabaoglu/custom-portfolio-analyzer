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

from data_struct import Asset, Price, Portfolio, PortfolioAsset


class DataLoader:
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(
        self,
        asset_data_path = 'data/fund_data.csv',
        portfolio_path = 'data/portfolio_config.json',
    ):
        self.asset_data_path = asset_data_path
        self.portfolio_path = portfolio_path

        self.assets_data = self.load_asset_data()
        self.portfolios = self.load_portfolios()

    def get_assets_data(self) -> List[Asset]:
        return self.assets_data

    def get_portfolios(self) -> List[Portfolio]:
        return self.portfolios

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

    def load_portfolios(self) -> List[Portfolio]:
        portfolios = []

        with open(self.portfolio_path, 'r', encoding='utf-8') as file:
            portfolio_data = json.load(file)

        for item in portfolio_data:
            assets = [
                PortfolioAsset(
                    asset=next(
                        (a for a in self.assets_data if a.get_code() == asset['code']),
                        None
                    ),
                    weight=asset['weight']
                )
                for asset in item['assets']
            ]

            portfolio = Portfolio(
                title=item['title'],
                start_date=datetime.strptime(item['start_date'], self.DATE_FORMAT),
                end_date=datetime.strptime(item['end_date'], self.DATE_FORMAT),
                assets=assets,
            )
            portfolios.append(portfolio)

        return portfolios
