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


from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import date

    from data_struct import PortfolioAsset, Portfolio


from collections import defaultdict
from typing import List, Dict, Tuple

from data_struct import Asset, DateRange, PerformanceReturn
from utils import DateUtils


class PortfolioPerformance:
    @staticmethod
    def generate_performance_info(portfolio: Portfolio) -> Dict:
        portfolio_title = portfolio.get_title()
        portfolio_code = ''.join(word[0].upper() for word in portfolio_title.split())
        performance_returns = PortfolioPerformance.after_tax_time_weighted_return(portfolio.get_assets())

        performance_info = {
            'portfolio_code': portfolio_code,
            'portfolio_title': portfolio_title,
            'performance_returns': performance_returns,
            'is_set_default': portfolio.is_set_default(),
        }
        return performance_info

    @staticmethod
    def after_tax_time_weighted_return(process_assets: List[PortfolioAsset]) -> List[PerformanceReturn]:
        """Time-Weighted Return (TWR) with cash flows (buys/sells) and per-asset tax on positive period gains."""
        if not process_assets:
            return []

        # Collect unique assets, tax rates, and transactions by day
        txs_by_day: Dict[date, List[Tuple[Asset, float]]] = defaultdict(list)
        unique_assets: List[Asset] = []
        seen_assets = set()
        earliest_tx_date: date = None

        # Gather transactions and unique assets
        for process_asset in process_assets:
            asset = process_asset.get_asset()

            if id(asset) not in seen_assets:
                seen_assets.add(id(asset))
                unique_assets.append(asset)

            txs_by_day[process_asset.get_order_date()].append((asset, process_asset.get_share()))

            if earliest_tx_date is None or process_asset.get_order_date() < earliest_tx_date:
                earliest_tx_date = process_asset.get_order_date()

        # Gather asset tax rates
        tax_rate_of_asset: Dict[Asset, float] = {
            asset: asset.get_additional_info().get_withholding_tax_rate()
            for asset in unique_assets
        }

        # Build asset price dictionaries
        price_map: Dict[Asset, Dict[date, float]] = {}
        date_sets: List[set] = []
        tx_date_range = DateRange(earliest_tx_date, DateUtils.get_today())

        # Collect all dates with available prices
        for asset in unique_assets:
            price_map[asset] = {
                price.get_date(): price.get_value()
                for price in asset.get_prices(tx_date_range)
            }
            date_sets.append({
                date
                for date in price_map[asset].keys()
            })
        dates = sorted(set.union(*date_sets))

        # State for TWR computation
        shares: Dict[Asset, float] = {asset: 0.0 for asset in unique_assets}
        cost_basis: Dict[Asset, float] = {asset: 0.0 for asset in unique_assets}
        prev_market_value: Dict[Asset, float] = {asset: 0.0 for asset in unique_assets}  # previous end of day MV
        cumulative = 1.0
        cumulative_return_series: List[float] = []

        # First day setup
        curr_date = dates.pop(0)
        price_today = {asset: price_map[asset].get(curr_date, 0.0) for asset in unique_assets}

        # Apply any transactions on the first day
        for (asset, delta) in txs_by_day.get(curr_date, []):
            shares[asset] += delta

        # Compute initial market values and cost basis
        for asset in unique_assets:
            market_value = shares[asset] * price_today[asset]
            prev_market_value[asset] = market_value
            cost_basis[asset] = market_value

        # Set baseline 0%
        cumulative_return_series.append(PerformanceReturn(
            date=curr_date,
            return_percentage_raw=0.0,
            return_percentage_tax_applied=0.0,
        ))

        # TWR computation loop
        for curr_date in dates:
            # Portfolio start value is previous day's end-of-day NAV
            portfolio_value_start = sum(prev_market_value.values())
            price_today = {asset: price_map[asset].get(curr_date, 0.0) for asset in unique_assets}

            # Compute pre-flow before and after-tax gain
            total_mv_before_flows = 0.0
            total_atmv_before_flows = 0.0
            for asset in unique_assets:
                mv_before_flows = shares[asset] * price_today[asset]
                total_mv_before_flows += mv_before_flows

                unrealized_gain = mv_before_flows - cost_basis[asset]
                potential_tax = max(0, unrealized_gain) * tax_rate_of_asset[asset]
                atmv_before_flows = mv_before_flows - potential_tax
                total_atmv_before_flows += atmv_before_flows

            # TWR return
            daily_return = 0.0
            if portfolio_value_start != 0.0:
                daily_return = total_mv_before_flows / portfolio_value_start - 1.0

            # TWR after-tax return
            daily_return_tax = 0.0
            if portfolio_value_start != 0.0:
                daily_return_tax = total_atmv_before_flows / portfolio_value_start - 1.0

            # Update cumulative return chains
            cumulative_tax_applied = cumulative * (1.0 + daily_return_tax)
            cumulative = cumulative * (1.0 + daily_return)
            cumulative_return_series.append(PerformanceReturn(
                date=curr_date,
                return_percentage_raw=cumulative - 1.0,
                return_percentage_tax_applied=cumulative_tax_applied - 1.0,
            ))

            # Apply today's external cash flows at end of day
            for (asset, delta) in txs_by_day.get(curr_date, []):
                shares.setdefault(asset, 0.0)
                cost_basis.setdefault(asset, 0.0)

                # Sell flows
                if delta < 0.0 and shares[asset] != 0.0:
                    proportion_sold = abs(delta) / shares[asset]
                    cost_basis[asset] *= (1.0 - proportion_sold)

                # Buy flows
                elif delta > 0.0:
                    cost_basis[asset] += delta * price_today[asset]

                shares[asset] += delta

            # Compute end-of-day NAV
            for asset in unique_assets:
                prev_market_value[asset] = shares[asset] * price_today[asset]

        return cumulative_return_series
